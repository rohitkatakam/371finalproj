import os
import sys
import requests

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from botE_engine.knowledge import config

class ReasoningEngine:
    def __init__(self, query_frame):
        self.query_frame = query_frame

    def get_direct_SPARQL_query(self):
        if "GDP" in self.query_frame["predicate"]:
            gdp_calc = "P2132" if self.query_frame["predicate"] == "hasGDPPerCapita" else "P2131"
            return config.GDP_PER_CAP_QUERY_TEMPLATE.format(
                country_name=self.query_frame["subject"],
                gdpCalc=gdp_calc,
                year=self.query_frame["year"])
    

    def execute_direct_query(self):
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
                headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text[:400])
            return None
    
if __name__ == "__main__":
    query_frame = {
        "predicate": "hasGDP",
        "subject": "United States",
        "target_variable": "?gdp",
        "year": 2022,
        "unit": "USD"
    }
    reasoner = ReasoningEngine(query_frame)
    gdp_value = reasoner.execute_query()
    print(f"GDP for {query_frame['subject']} in {query_frame['year']}: {gdp_value}")