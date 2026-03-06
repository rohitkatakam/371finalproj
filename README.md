# Project proposal/readme

**Team members**: Rohit Katakam, Joshua Yao, Ronit Mehta, Noah Schulhof

**What are you trying to do? What kinds of reasoning are you trying to do, involving what sorts of knowledge?** 

We propose to extend an existing back-of-the-envelope (BotE) reasoning framework in the FIRE reasoning engine by connecting it to real-world data from Wikidata. Back-of-the-envelope problems ask for quantities that aren’t explicitly stored in the knowledge base, but can be reasonably computed based on what is there in the knowledge base. For example, we can ask “How much coffee in total is consumed in year X?” This probably won’t be explicitly contained in the knowledge base but can be computed given some info is there. We’ll implement two main types of reasoning: decomposition and analogical generalization. 

Our project focuses on two primary types of symbolic reasoning: **decomposition** and **analogical generalization**.

Decomposition involves breaking down complex, unknown variables into smaller components that are more likely to be present in the knowledge base. For example, we can regard “Total consumption” as a product of “Population” and “per capita consumption”, both of which are a lot more likely to be contained in a knowledge base than the original query. 

Analogical generalization attacks sparse data or lack of data points. If we’re missing some information, we traverse the ontology to find some similar entity or data point we can reasonably generalize/infer from. For example, if we want to ask “How much coffee does Belgium drink?” but we’re missing that point, we can look around for similar or related data points; “How much coffee does Western Europe drink?” or “How much coffee does the Czech Republic drink?” (a European country with a similar population) would be helpful.

**What resources will you need?**

Our project relies on several resources. The primary reasoning engine will be FIRE, which already provides mechanisms for representing BotE strategies as suggestions and tracking problem-solving progress using an AND/OR tree. The knowledge base will consist of facts retrieved from Wikidata, a large, publicly accessible semantic web knowledge graph.

To access this data, we will use SPARQL, the standard query language for semantic web databases. SPARQL queries will allow us to extract the numeric values necessary for decomposition and analogical generalization. For example, queries can retrieve population figures, per-capita consumption rates, or related data points for similar entities when specific values are missing. In our workflow, SPARQL serves as the interface between the semantic web knowledge base and the symbolic reasoning performed in FIRE.

Additionally, we will need examples of BotE questions to test our system, such as historical estimates of consumption or cost across countries and years. Existing literature on BotE reasoning, including [Paritosh’s](https://www.qrg.northwestern.edu/papers/Files/BotEStrategiesAAAI05Distrib.pdf) original BotE system and subsequent adaptations using semantic web resources, will guide the encoding of strategies and decomposition heuristics.

**What is your plan for carrying out your project?**

Our plan is to first identify a set of concrete BotE estimation problems and extract the relevant RDF subset from Wikidata. We will then encode decomposition and analogical generalization strategies as suggestions within FIRE. SPARQL queries will be used to retrieve the necessary data from Wikidata, which will then need to be connected to FIRE so that the reasoning engine can access the retrieved values during problem solving. After implementing these strategies and integrating SPARQL-based data retrieval, we will run example problems end-to-end to verify that the system can reason correctly and produce plausible ballpark estimates. We will then iteratively refine the strategies, optimize reasoning, and evaluate the accuracy and plausibility of the results.

*Weekly milestones:*

- Week 7 (Feb 12-18)  
  - *Goal*: verify that we can use wikidata and get all software environments running  
  - Audit wikidata to find specific content needed for our domain (**Rohit & Josh)**  
  - Create a list of “happy path” questions where the answer is known to use for testing (**Rohit & Josh**)  
  - Set up the FIRE reasoning engine environment  and test it works (**Ronit & Noah**)  
- Week 8 (Feb 19-25):  
  - *Goal:* System should be able to answer a question if the data exists directly/can be simply broken down  
  - Write the python wrapper that takes a query from FIRE and turns it into SPARQL (**Rohit & Ronit**)  
  - Implement normalizing units in python; if a user asks for usd but the data in wikidata is in eur, convert before returning it (**Josh & Noah**)  
- Week 9 (Feb 26-March 4)  
  - *Goal:* The system can handle missing data by guessing based on similar entities  
  - Implement the generalization strategy, logic that searches wikidata for related entities (**Josh & Ronit**)  
  - Run a full test on the happy path questions (**Rohit & Noah**)  
- Week 10 (March 5-9)  
  - *Goal*: Finalize results and deliverables (**Everyone**)  
  - Run the test suite again and record metrics  
  - Compile results into presentation

**What is the biggest risk?**

The primary risk is missing or incomplete data in Wikidata, which could prevent accurate decomposition or analogical inference. Another risk is ensuring that the SPARQL data retrieval pipeline integrates smoothly with FIRE, so that the reasoning engine can dynamically access values as needed. We will mitigate these risks by starting with a small, curated subset of Wikidata focused on a specific domain, such as food consumption or demographics, and expanding as we test and refine our reasoning strategies.

**What are your first actions on the project?**

Our initial actions will include selecting 5-10 concrete example problems, extracting the relevant RDF subset of Wikidata, and implementing initial strategies for decomposition and analogical generalization in FIRE. We will also prototype the connection between SPARQL-based data retrieval and FIRE so that the engine can access retrieved values during reasoning. Once these pieces are in place, we will test a few problems end-to-end to verify that the system produces reasonable back-of-the-envelope estimates. This incremental approach allows us to validate and refine the reasoning capabilities while remaining fully within a symbolic, knowledge-based framework.
