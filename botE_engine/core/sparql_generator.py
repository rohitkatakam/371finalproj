from botE_engine.knowledge import config

class SparQLGenerator:
    def __init__(self, query_frame):
        self.query_frame = query_frame
    
    def generate_SPARQL_query(self):
        '''Generates a SPARQL query based on the query frame, handling different predicates and properties.'''
        
        # Gets the property information based on what is stored in the config file for the given predicate
        properties_info = config.PROPERTIES.get(self.query_frame["predicate"])
        if not properties_info:
            print("Error: unsupported predicate in query frame")
            return None
        
        # Constructs the year filter if the property is year-dependent and a year is specified in the query frame
        year_filter = ""
        if properties_info.get("year_dependent") and self.query_frame["year"]:
            year_filter = f"""
            pq:P585 ?date.
            FILTER(YEAR(?date) = {self.query_frame['year']})
            """
        
        # Builds the base SPARQL query, including the optional economy check if specified in the property information
        base_query = f""" SELECT {self.query_frame['target_variable']} WHERE {{ 
        ?country wdt:P31 wd:Q6256;
        rdfs:label "{self.query_frame['subject']}"@en.
        {{
            ?country p:{properties_info['id']} ?statement.
            ?statement ps:{properties_info['id']} {self.query_frame['target_variable']};
            
            {year_filter}


        }} """ 
        
        

        if properties_info["add_economy_check"]:
            base_query += f"""
            UNION
            {{
                ?economy wdt:P31 wd:Q6456916;
                         wdt:P276 ?country.
                ?economy p:{properties_info['id']} ?statement.
                ?statement ps:{properties_info['id']} {self.query_frame['target_variable']};
                    {year_filter}
            }} """

        return base_query + "}"
