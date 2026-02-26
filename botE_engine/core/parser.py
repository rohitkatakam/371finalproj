import re


class FireQueryParser:
    def __init__(self, query):
        self.raw_query = query.strip()
        self.parsed_tree = self.set_variable_mapping()

    def parse_to_list(self):
        tokens = self.raw_query.replace("(", "").replace(")", "").split()
        return tokens
    
    def get_query_frame(self):
        tokens = self.parse_to_list()
        
        frame = {
            "predicate": tokens[0],
            "subject": tokens[1],
            "target_variable": None,
            "year": None,
            "unit": "USD" 
        }

        for t in tokens:
            if t.startswith("?"):
                frame["target_variable"] = t
            elif t.isdigit() and len(t) == 4:
                frame["year"] = int(t)
            elif t.isupper() and len(t) == 3:
                frame["unit"] = t
        
        return frame
    
    def count_uppercase_sum(self, input_string):
        return sum(char.isupper() for char in input_string)
    
    def set_variable_mapping(self):
        frame = self.get_query_frame()

        print(frame["subject"])

        if frame["predicate"] == "hasGDPPerCapita" or frame["predicate"] == "hasGDP":
            if self.count_uppercase_sum(frame["subject"]) >= 2:
                frame["subject"] = re.sub(r'(\w)([A-Z])', r'\1 \2', frame["subject"]).strip()

        return frame
            
        