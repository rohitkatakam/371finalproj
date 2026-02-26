from botE_engine.knowledge import config

class SparQLGenerator:
    def __init__(self, query_frame):
        self.query_frame = query_frame
    
    def generate_SPARQL_query(self):
        '''Generates a SPARQL query based on the query frame, handling different predicates and properties.'''
        properties_info = config.PROPERTIES.get(self.query_frame["predicate"])
        if not properties_info:
            print("Error: unsupported predicate in query frame")
            return None
        
        base_query = f""" SELECT {self.query_frame['target_variable']} WHERE {{ 
        ?country wdt:P31 wd:Q6256;
        rdfs:label "{self.query_frame['subject']}"@en.
        {{
            ?country p:{properties_info['id']} ?statement.
            ?statement ps:{properties_info['id']} {self.query_frame['target_variable']};
                                pq:P585 ?date.
                FILTER(YEAR(?date) = {self.query_frame['year']})
        }} """ 

        if properties_info["add_economy_check"]:
            base_query += f"""
            UNION
            {{
                ?economy wdt:P31 wd:Q6456916;
                         wdt:P276 ?country.
                ?economy p:{properties_info['id']} ?statement.
                ?statement ps:{properties_info['id']} {self.query_frame['target_variable']};
                                   pq:P585 ?date.
                FILTER(YEAR(?date) = {self.query_frame['year']})
            }} """

        return base_query + "}"
