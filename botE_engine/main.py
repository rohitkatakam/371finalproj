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
        print("--------Running query through botE engine--------")

        # Step 1: Parse the query to extract components
        print(f"Received query: {query}")
        parser = FireQueryParser(query)
        query_frame = parser.parsed_tree

        # Step 2: Attempt direct retrieval of data from Wikidata
        reasoner = ReasoningEngine()
        data = reasoner.execute_direct_query(query_frame)

        # If successful, return the value
        result = reasoner.get_result_from_json(data, query_frame)
        if result is not None:
            print("----------------")
            return result
            
        # Fallback to decomposition reasoning if direct retrieval fails
        print("Direct retrieval failed, attempting decomposition reasoning...")
        result = reasoner.complete_decomposition_reasoning(query_frame)
        if result is not None:
            print("----------------")
            return result
        

        # Move to analogical reasoning
        pass


if __name__ == "__main__":
    query = "(hasPopulationDensity Finland ?x 2017 USD)"
    main_engine = MainEngine()
    value = main_engine.run_query(query)
    print(value)
        