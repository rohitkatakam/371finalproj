import requests

from botE_engine.knowledge import config
from botE_engine.core.sparql_generator import SparQLGenerator

class ReasoningEngine:  

    def get_result_from_json(self, result, query_frame):
        if result and "results" in result and "bindings" in result["results"]:
            bindings = result["results"]["bindings"]
            if len(bindings) > 0:
                var_name = query_frame["target_variable"].replace("?", "")
                if var_name in bindings[0]:
                    return bindings[0][var_name]["value"]  
        return None

    
    def execute_direct_query(self, query_frame):
        '''Executes the SPARQL query against the Wikidata endpoint and returns the results.'''
        print(f"Executing direct SPARQL query for frame: {query_frame}")

        sparql_generator = SparQLGenerator(query_frame)
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
    
    def complete_decomposition_reasoning(self, query_frame):
        '''Performs decomposition reasoning by breaking down the query into sub-queries and computing results'''
        sub_factors = config.PROPERTIES[query_frame["predicate"]].get("decomposition_method", {})
        if not sub_factors:
            print("No decomposition factors defined for this predicate.")
            return None
        
        # Division-based decomposition reasoning
        if sub_factors["operation"] == "division":
            numerator_frame = query_frame.copy()
            numerator_frame["predicate"] = sub_factors["numerator"]
            denominator_frame = query_frame.copy()
            denominator_frame["predicate"] = sub_factors["denominator"]

            numerator_result = self.execute_direct_query(numerator_frame)
            denominator_result = self.execute_direct_query(denominator_frame)

            if not numerator_result or not denominator_result:
                print("Error retrieving data for decomposition.")
                return None
            
            # Extract values from results (this is simplified and may need more robust handling)
            try:
                num_value = float(self.get_result_from_json(numerator_result, numerator_frame))
                denom_value = float(self.get_result_from_json(denominator_result, denominator_frame))
                if denom_value == 0:
                    print("Error: Division by zero in decomposition.")
                    return None
                return num_value / denom_value
            except (KeyError, IndexError, ValueError) as e:
                print(f"Error processing decomposition results: {e}")
                return None
        
        # Multiplication-based decomposition reasoning
        pass

        
        