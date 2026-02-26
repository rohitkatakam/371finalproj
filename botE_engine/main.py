try:
    from botE_engine.core.parser import FireQueryParser
    from botE_engine.core.reasoner import ReasoningEngine
except ModuleNotFoundError:
    import os
    import sys

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    from botE_engine.core.parser import FireQueryParser
    from botE_engine.core.reasoner import ReasoningEngine


class MainEngine:
    def run_query(self, query):

        # Step 1: Parse the query to extract components
        parser = FireQueryParser(query)
        query_frame = parser.parsed_tree

        # Step 2: Attempt direct retrieval of data from Wikidata
        reasoner = ReasoningEngine(query_frame)
        result = reasoner.execute_direct_query()

        # If successful, return the value
        if result and "results" in result and "bindings" in result["results"]:
            bindings = result["results"]["bindings"]
            if len(bindings) > 0:
                var_name = query_frame["target_variable"].replace("?", "")
                if var_name in bindings[0]:
                    return bindings[0][var_name]["value"]
            
        # Fallback to complex reasoning (Decomposition/Aggregation)
        pass

if __name__ == "__main__":
    query = "(hasPopulation UnitedStates ?population 1970 USD)"
    main_engine = MainEngine()
    value = main_engine.run_query(query)
    print(value)
        