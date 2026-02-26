#Wikidata endpoint for making the SPARQL queries
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

#Constants for GDP calculations
GDP_PER_CAPITA_PROPERTY = "P2132"
GDP_PROPERTY = "P2131"
GDP_PPP_PROPERTY = "P4010"

PROPERTIES = {
    "hasGDPPerCapita": {"id": GDP_PER_CAPITA_PROPERTY, "add_economy_check": True, "year_dependent": True, "decomposition_method": {"operation": "division", "numerator": "hasGDP", "denominator": "hasPopulation"}},
    "hasGDP": {"id": GDP_PROPERTY, "add_economy_check": True, "year_dependent": True},
    "hasGDPPPP": {"id": GDP_PPP_PROPERTY, "add_economy_check": True, "year_dependent": True},
    "hasPopulation": {"id": "P1082", "add_economy_check": False, "year_dependent": True},
    "hasArea": {"id": "P2046", "add_economy_check": False, "year_dependent": False},
    "hasPopulationDensity": {"id": "P1083", "add_economy_check": False, "year_dependent": True, "decomposition_method": {"operation": "division", "numerator": "hasPopulation", "denominator": "hasArea"}}
}