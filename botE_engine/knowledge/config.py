#Wikidata endpoint for making the SPARQL queries
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

#SPARQL query template for retrieving GDP data from Wikidata
DIRECT_GDP_QUERY_TEMPLATE = """
SELECT ?countryLabel ?finalGDP WHERE {{
  ?country wdt:P31 wd:Q6256;
           rdfs:label "{country_name}"@en.

  {{
    ?country p:{gdpCalc} ?statement.
    ?statement ps:{gdpCalc} ?gdpValue;
               pq:P585 ?date.
    FILTER(YEAR(?date) = {year})
  }}
  UNION
  {{
    ?economy wdt:P31 wd:Q6456916;
             wdt:P131 ?country.
    
    ?economy p:{gdpCalc} ?statement.
    ?statement ps:{gdpCalc} ?gdpValue;
               pq:P585 ?date.
    FILTER(YEAR(?date) = {year})
  }}

  BIND(?gdpValue AS ?finalGDP)
  
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
LIMIT 1
"""

#Constants for GDP calculations
GDP_PER_CAPITA_PROPERTY = "P2132"
GDP_PROPERTY = "P2131"
GDP_PPP_PROPERTY = "P4010"