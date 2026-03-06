from companionsKQML import Pythonian, listify
from kqml import KQMLPerformative
import logging
import threading
import re
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SPARQL_values = {
    "population": 
        {
            "id": "P1082", 
            "year_dependent": True, 
            "add_economy_check": False
         },
            
    "gdp": 
        {
            "id": "P2131", 
            "year_dependent": True, 
            "add_economy_check": True
        },
            
    "gdppercapita": 
        {
            "id": "P2132", 
            "year_dependent": True, 
            "add_economy_check": True
         },
    
    "unemploymentrate":
        {
            "id": "P1198", 
            "year_dependent": True, 
            "add_economy_check": True
         }
    
}

def generate_SPARQL_query(country, year, prop, mereology=False):
        # Generates a SPARQL query based on the input country, year, and property. It uses the SPARQL_values dictionary to determine how to construct the query for different properties.
        
        logger.info(f"Generating SPARQL query for country/entity: {country}, year: {year}, property: {prop}")
        country = country_spacer(country)
        logger.info(f"Formatted country/entity name for SPARQL query: {country}")
        
        
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
        base_query = f"""SELECT {"?country ?countryLabel" if mereology else ""} ?value WHERE {{
        {
        f"?country wdt:P31 wd:Q6256; rdfs:label '{country}'@en."
        if not mereology else
        f"?org rdfs:label '{country}'@en . ?country wdt:P463 ?org ; wdt:P31 wd:Q6256 ."
        }
        {{
        ?country p:{properties_info['id']} ?statement.
        ?statement ps:{properties_info['id']} ?value;
        {year_filter}
        }}"""
        
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
    
def analogical_query_generation(country, year):
    country = country_spacer(country)
    logger.info(f"Generating analogical SPARQL query for country: {country}, year: {year}")
    query = f""" SELECT ?similar_country ?similar_countryLabel ?value2
    WHERE {{
           ?country wdt:P31 wd:Q6256 ;
           rdfs:label "{country}"@en ;
           p:P1081 ?statement_us ;
           p:P1082 ?statement4.

            ?statement_us ps:P1081 ?value ;
                           pq:P585 ?date1 .
            FILTER(YEAR(?date1) = {year})
  
             ?statement4 ps:P1082 ?value4 ;
             pq:P585 ?date4 .
             FILTER(YEAR(?date4) = {year})
 
            ?similar_country wdt:P31 wd:Q6256 ;
                   p:P1081 ?statement2;
                   p:P1082 ?statement3.

            ?statement2 ps:P1081 ?value2 ;
              pq:P585 ?date2 .
            FILTER(YEAR(?date2) = {year})
  
            ?statement3 ps:P1082 ?value3 ;
             pq:P585 ?date3 .
            FILTER(YEAR(?date3) = {year})
      

            FILTER(?similar_country != ?country)

            FILTER(ABS(?value2 - ?value) <= 0.1)
            FILTER(?value3 > ?value4 / 3)
            FILTER(?value3 < ?value4 * 3)

             SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
            }}
            ORDER BY (ABS(?value2 - ?value))
            LIMIT 1"""
    return query
    
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
    n = count_uppercase_sum(country)
    if n >= 2 and n != len(country):
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

def get_similar_country_from_json(result):
    # Extracts the similar country from the analogical SPARQL query result JSON.
    if result and "results" in result and "bindings" in result["results"]:
        bindings = result["results"]["bindings"]
        if len(bindings) > 0:
            var_name = "similar_countryLabel"
            if var_name in bindings[0]:
                logger.info(f"Extracted similar country: {bindings[0][var_name]['value']}")
                name = bindings[0][var_name]["value"]
                name = name.replace(" ", "")
                return name 
    return None


class EconomicsAgent(Pythonian):
    name = "EconomicsAgent"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debug = True
        self.add_ask(self.wikidata_lookup, name="wikidataLookup")
        self.advertise("(wikidataLookup ?country ?year ?property ?result)")
        self.add_ask(self.analogical_query, name="analogicalLookup")
        self.advertise("(analogicalLookup ?country ?year ?returnedcountry)")
        self.add_ask(self.convert_units, name="convertUnits")
        self.advertise("(convertUnits ?fromUnit ?toUnit ?year ?factor)")
        self.add_ask(self.mereology_lookup, name="mereologyLookup")
        self.advertise("(mereologyLookup ?organization ?year ?property ?values)")
        
    @staticmethod
    def mereology_lookup(organization, year, prop):
        logger.info(f"mereology_lookup called with: {organization}")

        organization = str(organization)
        organization = country_spacer(organization)
        
        logger.info(f"Formatted organization name for SPARQL query: {organization}")

        prop = str(prop)
        SPARQL_query = generate_SPARQL_query(organization, year, prop.lower(), mereology=True)
        if SPARQL_query is None:
            logger.error("Error: Failed to generate SPARQL query for mereology lookup.")
            return None
        
        result = execute_direct_query(SPARQL_query)
        if result is None:
            logger.error("Error: Failed to execute SPARQL query for mereology lookup.")
            return None
        
        logger.info(f"SPARQL query result for mereology lookup: {result}")
        values = []
        countries = set()
        if result and "results" in result and "bindings" in result["results"]:
            bindings = result["results"]["bindings"]
            for binding in bindings:
                if "value" in binding:
                    if binding['country']['value'] not in countries:
                        countries.add(binding['country']['value'])
                        values.append(binding["value"]["value"])
        
        return values

    @staticmethod
    def wikidata_lookup(country, year, prop):
        logger.info(f"wikidata_lookup called with: {country}, {year}, {prop}")

        # Turn input into strings
        country = str(country)
        year = str(year)
        prop = str(prop)
        
        # Generate the SPARQL query based on the input parameters
        SPARQL_query = generate_SPARQL_query(country, year, prop.lower(), mereology=False)
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
    
    @staticmethod
    def analogical_query(country, year):
        logger.info(f"analogical_query called with: {country}, {year}")

        # Turn input into strings
        country = str(country)
        year = str(year)
        
        # Generate the analogical SPARQL query based on the input parameters
        SPARQL_query = analogical_query_generation(country, year)
        if SPARQL_query is None:
            logger.error("Error: Failed to generate analogical SPARQL query.")
            return None
        
        # Execute the analogical SPARQL query and get the results
        result = execute_direct_query(SPARQL_query)
        if result is None:
            logger.error("Error: Failed to execute analogical SPARQL query.")
            return None
        
        logger.info(f"Analogical SPARQL query result: {result}")
        # Extract the similar country from the analogical SPARQL query result
        similar_country = get_similar_country_from_json(result)
        if similar_country is None:
            logger.info("No similar country found for the query.")
            return None
        
        return similar_country
    
    
    @staticmethod
    def convert_units(from_unit, to_unit, year):
        logger.info(f"convert_units called with: {from_unit}, {to_unit}, {year}")

        from_unit = str(from_unit).upper()
        to_unit = str(to_unit).upper()
        year = str(year)

        if from_unit == to_unit:
            return "1"

        # Use frankfurter.app for historical exchange rates (free, no API key needed)
        try:
            url = f"https://api.frankfurter.app/{year}-01-01"
            response = requests.get(url, params={"from": from_unit, "to": to_unit})
            if response.status_code == 200:
                data = response.json()
                rate = data.get("rates", {}).get(to_unit)
                if rate is not None:
                    logger.info(f"Exchange rate {from_unit}->{to_unit} for {year}: {rate}")
                    return str(rate)
            logger.error(f"Frankfurter API error {response.status_code}: {response.text[:200]}")
        except Exception as e:
            logger.error(f"Error fetching exchange rate: {e}")

        return None

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
            if isinstance(results, list):
                results = listify(results)
            content_str = f'((({var_name} . {results})))'
            
        print(f"Formatted content string for KQML response: {content_str}")
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
