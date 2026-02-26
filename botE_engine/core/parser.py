import re

class FireQueryParser:
    def __init__(self, query):
        self.raw_query = query.strip()
        self.parsed_tree = self.get_query_frame()

    def parse_to_list(self):
        '''Converts the raw query string into a list of tokens, removing parentheses.'''
        tokens = self.raw_query.replace("(", "").replace(")", "").split()
        return tokens
    
    def get_query_frame(self):
        '''Constructs a query frame (dictionary) from the list of tokens, 
        identifying the predicate, subject, target variable, year, and unit.'''

        tokens = self.parse_to_list()
        if len(tokens) < 2:
            raise ValueError("Query must include at least predicate and subject")

        frame = {"predicate": tokens[0], "subject": tokens[1], "target_variable": None, "year": None, "unit": "USD" }
        
        for t in tokens:
            if t.startswith("?"):
                frame["target_variable"] = t
            elif t.isdigit() and len(t) == 4:
                frame["year"] = int(t)
            elif t.isupper() and len(t) == 3:
                frame["unit"] = t

        if self.count_uppercase_sum(frame["subject"]) >= 2:
            frame["subject"] = re.sub(r'(\w)([A-Z])', r'\1 \2', frame["subject"]).strip()

        print(f"Parsed query frame: {frame}")
        return frame
    
    def count_uppercase_sum(self, input_string):
        '''Counts the number of uppercase letters in the input string.'''
        return sum(char.isupper() for char in input_string)
            
        