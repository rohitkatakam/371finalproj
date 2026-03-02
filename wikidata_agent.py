from companionsKQML import Pythonian
from kqml import KQMLPerformative
import logging
import time
import threading
import re
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SPARQL_values = {
            "population": {"id": "P1082", "year_dependent": True, "add_economy_check": False},
            "gdp": {"id": "P2131", "year_dependent": True, "add_economy_check": True},
            "gdppercapita": {"id": "P2132", "year_dependent": True, "add_economy_check": True}
}

def generate_SPARQL_query(country, year, prop):
        # Generates a SPARQL query based on the input country, year, and property. It uses the SPARQL_values dictionary to determine how to construct the query for different properties.
        
        logger.info(f"Generating SPARQL query for country: {country}, year: {year}, property: {prop}")
        country = country_spacer(country)
        logger.info(f"Formatted country name for SPARQL query: {country}")
        
        
        # Gets the property information based on what is stored in the config file for the given predicate
        properties_info = SPARQL_values.get(prop)
        if not properties_info:
            logger.error("Error: missing property")
            return None
        
        logger.info(f"Using property information for SPARQL query: {properties_info}")
        
        # Add the year filter if the property is year-dependent
        year_filter = ""
        if properties_info.get("year_dependent"):
            logger.info(f"Property {prop} is year-dependent, adding year filter for SPARQL query.")
            year_filter = f"""
            pq:P585 ?date.
            FILTER(YEAR(?date) = {year})
            """
        
        # Builds the query
        base_query = f""" SELECT ?value WHERE {{ 
        ?country wdt:P31 wd:Q6256;
        rdfs:label "{country}"@en.
        {{
            ?country p:{properties_info['id']} ?statement.
            ?statement ps:{properties_info['id']} ?value;
            
            {year_filter}


        }} """ 
        
        if properties_info["add_economy_check"]:
            base_query += f"""
            UNION
            {{
                ?economy wdt:P31 wd:Q6456916;
                         wdt:P276 ?country.
                ?economy p:{properties_info['id']} ?statement.
                ?statement ps:{properties_info['id']} ?value;
                    {year_filter}
            }} """

        return base_query + "}"
    
def execute_direct_query(SQARQL_query):
    # API Call to Wikidata with Sparql query
    headers = { "User-Agent": "botE/1.0 (contact: ronitmehta1@gmail.com)", "Accept": "application/sparql-results+json; charset=utf-8" }
    response = requests.get("https://query.wikidata.org/sparql", params={"query": SQARQL_query, "format": "json"}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logger.error(f"Error: {response.status_code}")
        logger.error(response.text[:400])
        return None

def country_spacer(country):
    # If the country name has 2 or more uppercase letters, assume it's in camel case and add spaces before uppercase letters.
    if count_uppercase_sum(country) >= 2:
        return re.sub(r'(\w)([A-Z])', r'\1 \2', country.strip())
    return country

def count_uppercase_sum(input_string):
    # Counts the number of uppercase letters in the input string.
    return sum(char.isupper() for char in input_string)

def get_result_from_json(result):
    # Extracts the relevant value from the SPARQL query result JSON.
    if result and "results" in result and "bindings" in result["results"]:
        bindings = result["results"]["bindings"]
        if len(bindings) > 0:
            var_name = "value"
            if var_name in bindings[0]:
                logger.info(f"Extracted value: {bindings[0][var_name]['value']}")
                return bindings[0][var_name]["value"]  
    return None


class EconomicsAgent(Pythonian):
    name = "EconomicsAgent"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debug = True
        self.add_ask(self.wikidata_lookup, name="wikidataLookup")
        self.advertise("(wikidataLookup ?country ?year ?property ?result)")

    @staticmethod
    def wikidata_lookup(country, year, prop):
        logger.info(f"wikidata_lookup called with: {country}, {year}, {prop}")

        # Turn input into strings
        country = str(country)
        year = str(year)
        prop = str(prop)
        
        # Generate the SPARQL query based on the input parameters
        SPARQL_query = generate_SPARQL_query(country, year, prop.lower())
        if SPARQL_query is None:
            logger.error("Error: Failed to generate SPARQL query.")
            return None
        
        # Execute the SPARQL query and get the results
        result = execute_direct_query(SPARQL_query)
        if result is None:
            logger.error("Error: Failed to execute SPARQL query.")
            return None
        
        logger.info(f"SPARQL query result: {result}")
        
        # Extract the relevant value from the SPARQL query result
        answer = get_result_from_json(result)
        if answer is None:
            logger.info("No results found for the query.")
            return None   
         
        return answer
    
    
    def receive_ask_all(self, msg, content):
        # Ask all doesn't work so use ask one
        logger.info(f"receive_ask_all called with: {content}")
        self.receive_ask_one(msg, content)
    
    
    def receive_eof(self):
        #Stops weird printing issue
        pass
    
    def response_to_query(self, msg, content, results, response_type):
        logger.info(f"Responding to query with results: {results}")
        logger.debug('Responding to query: %s, %s, %s', msg, content, results)
        
        # Format the results as bindings bc other way didn't work
        if results is None:
            content_str = '()'
        else: 
            #create binding based on module function but no predicate
            var_name = None
            for each in content.data[1:]:
                if str(each).startswith('?'):
                    var_name = str(each)
            var_name = var_name or '?result'
            content_str = f'((({var_name} . {results})))'
            
        reply_msg = (f'(tell :sender {self.name} :content {content_str})')
        self.reply(msg, KQMLPerformative.from_string(reply_msg))

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    AGENT = EconomicsAgent.parse_command_line_args()
    
    try:
        # keeps it running otherwise it just ends on it own
        threading.Event().wait()
    except KeyboardInterrupt:
        logger.info("Shutting down agent...")
        AGENT.shutdown()
