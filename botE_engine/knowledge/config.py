#Wikidata endpoint for making the SPARQL queries
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

#SPARQL query template for retrieving GDP data from Wikidata
GDP_PER_CAP_QUERY_TEMPLATE = """
SELECT ?countryLabel ?finalGDP WHERE {{
  # 1. Find the Country
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

