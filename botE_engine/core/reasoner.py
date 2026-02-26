import requests

from botE_engine.knowledge import config

class ReasoningEngine:
    def __init__(self, query_frame):
        self.query_frame = query_frame

    def get_direct_SPARQL_query(self):
        '''Constructs a SPARQL query based on the query frame for direct retrieval of GDP data from Wikidata.'''
        if "GDP" in self.query_frame["predicate"]:
            if "PerCapita" in self.query_frame["predicate"]:
                gdp_calc = config.GDP_PER_CAPITA_PROPERTY
            elif "PPP" in self.query_frame["predicate"]:
                gdp_calc = config.GDP_PPP_PROPERTY
            else:
                gdp_calc = config.GDP_PROPERTY


            return config.DIRECT_GDP_QUERY_TEMPLATE.format(
                country_name=self.query_frame["subject"],
                gdpCalc=gdp_calc,
                year=self.query_frame["year"],
                target_variable=self.query_frame["target_variable"])
    

    def execute_direct_query(self):
        '''Executes the SPARQL query against the Wikidata endpoint and returns the results.'''
        sparql_query = self.get_direct_SPARQL_query()
        if not sparql_query:
            print("Error: unsupported predicate in query frame")
            return None

        headers = {
            "User-Agent": "botE/1.0 (contact: ronitmehta1@gmail.com)",
            "Accept": "application/sparql-results+json; charset=utf-8" 
        }

        response = requests.get(
                config.WIKIDATA_SPARQL_ENDPOINT,
                params={"query": sparql_query, "format": "json"},
                headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text[:400])
            return None