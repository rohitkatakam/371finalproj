# Happy Path Questions: BotE Reasoning Test Suite

## 1. Decompositional Reasoning
*Goal: Break down a target variable into constituent parts that exist in the knowledge base.*

* **Query Example:** "What was the GDP/Capita of South Africa in 2017?"
* **Intended Answer:** Around $6,302.08
* **Predicate Calculus:** `(hasEconomicValue SouthAfrica 2017 GDPPerCapita ?GDPPerCapita)`
* **FIRE Strategy:** GDP per Capita = Total GDP ÷ Population. 
* **Current Progress:** **Completed.** 

## 2. Analogical Reasoning (Missing Data)
*Goal: Traverse the ontology to find a similar entity to infer missing data points.*

* **Query Example:** "What was the GDP/Capita of Somalia in 2012?"
* **Intended Answer:** ~$468 (Inferred using Ethiopian GDP/Capita)
* **Predicate Calculus:** `(hasEconomicValue Somalia 2012 GDPPerCapita ?GDPPerCapita)`
* **FIRE Strategy:** Identify sparse/missing data for the target entity, traverse Wikidata's region and subclass links to find a comparable neighbor (e.g., Ethiopia), and apply its economic metrics to the target.
* **Current Progress:** **Completed.** Fails when no other country has an HDI score within 0.1, and a population within 1/3 to 3x that of the queried country.

## 3. Mereology (Addition / Aggregation)
*Goal: Compute the output of a macro-entity by aggregating the outputs of its constituent parts.*

* **Query Example:** "What was the population of the European Union in 2022?"
* **Intended Answer:** ~446 million
* **Predicate Calculus:** `(hasEconomicValue EuropeanUnion 2022 Population ?Population)`
* **FIRE Strategy:** Identify constituent members of the macro-entity and sum their individual values for the specified year.
* **Current Progress:** **Completed.** 

## 4. Unit Conversion
*Goal: Dynamically convert economic outputs into requested currencies or scales.*

* **Query Example:** "What is the GDP/Capita of Turkey in 2022 in Lira?"
* **Intended Answer:** ~38,500 Turkish Lira
* **Predicate Calculus:** `(hasEconomicValueInUnit Turkey 2022 GDPPerCapita ?GDPPerCapita TRY)`
* **FIRE Strategy:** Retrieve the base economic value and its unit metadata, then apply a conversion factor to output the requested currency (TRY).
* **Current Progress:** **Completed.** 