import requests

from botE_engine.knowledge import config
from botE_engine.core.sparql_generator import SparQLGenerator

class ReasoningEngine:
    def __init__(self, query_frame):
        self.query_frame = query_frame
    

    def execute_direct_query(self):
        '''Executes the SPARQL query against the Wikidata endpoint and returns the results.'''
        sparql_generator = SparQLGenerator(self.query_frame)
        sparql_query = sparql_generator.generate_SPARQL_query()
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