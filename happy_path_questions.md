# Happy Path Questions: BotE Reasoning Test Suite

## 1. Decompositional Reasoning
*Goal: Break down a target variable into constituent parts that exist in the knowledge base.*

* **Query Example:** "What was the GDP/Capita of South Africa in 2017?"
* **Intended Answer:** Around $6,302.08
* **Predicate Calculus:** `(hasGDPPerCapita SouthAfrica ?value 2017 USD)`
* **FIRE Strategy:** GDP per Capita = Total GDP ÷ Population. 
* **Current Progress:** **In Progress.** Relevant Wikidata properties for GDP and population have been identified and validated. SPARQL queries successfully retrieve these values. The initial Python wrapper is implemented, and decomposition rules are currently being encoded in FIRE to compute the division when direct values are missing.

## 2. Analogical Reasoning (Missing Data)
*Goal: Traverse the ontology to find a similar entity to infer missing data points.*

* **Query Example:** "What was the GDP/Capita of Somalia in 2012?"
* **Intended Answer:** Around $468 (Inferred using Ethiopian GDP/Capita)
* **Predicate Calculus:** `(hasGDPPerCapita Somalia ?value 2012 USD)`
* **FIRE Strategy:** Identify sparse/missing data for the target entity, traverse Wikidata's region and subclass links to find a comparable neighbor (e.g., Ethiopia), and apply its economic metrics to the target.
* **Current Progress:** **In Progress.** Sparse GDP coverage for certain countries has been confirmed. Exploration of Wikidata’s ontology (specifically region and subclass links) is underway to support the analogical lookup logic.

## 3. Mereology (Addition / Aggregation)
*Goal: Compute the output of a macro-entity by aggregating the outputs of its constituent parts.*

* **Query Example:** "What is the GDP (PPP) of BRICS in 2022?"
* **Intended Answer:** Around 25 trillion USD
* **Predicate Calculus:** `(hasGDP ?x BRICS)`
* **FIRE Strategy:** Identify constituent members of the BRICS organization and sum their individual GDP (PPP) values for the specified year.
* **Current Progress:** **In Progress.** GDP (PPP) coverage for BRICS member countries is verified, and SPARQL retrieval is working. Aggregation rules are actively being implemented in the wrapper to sum member values. Testing is focused on year alignment and handling missing data among member states.

## 4. Unit Conversion
*Goal: Dynamically convert economic outputs into requested currencies or scales.*

* **Query Example:** "What is the GDP/Capita of Turkey in 2022 in Lira?"
* **Intended Answer:** ~15 trillion Turkish Lira
* **Predicate Calculus:** `(hasGDPPerCapita Turkey ?value 2022 TRY)`
* **FIRE Strategy:** Retrieve the base economic value and its unit metadata, then apply a conversion factor to output the requested currency (TRY).
* **Current Progress:** **In Progress.** Confirmed that economic values in Wikidata include unit metadata retrievable via SPARQL. If historical