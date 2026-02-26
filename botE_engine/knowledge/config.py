#Wikidata endpoint for making the SPARQL queries
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

#Constants for GDP calculations
GDP_PER_CAPITA_PROPERTY = "P2132"
GDP_PROPERTY = "P2131"
GDP_PPP_PROPERTY = "P4010"

PROPERTIES = {
    "hasGDPPerCapita": {"id": GDP_PER_CAPITA_PROPERTY, "add_economy_check": True},
    "hasGDP": {"id": GDP_PROPERTY, "add_economy_check": True},
    "hasGDPPPP": {"id": GDP_PPP_PROPERTY, "add_economy_check": True},
    "hasPopulation": {"id": "P1082", "add_economy_check": False},
}