# Instructions for Running Agent in Companions

1. Download the run-companions script, agent file, and .krf file

2. Make sure you have local directory *companions*. You may have to run the run-companions script once to generate all of the folders inside of it.

2. Place agent file into companions -> pythonian folder

3. In your run-companions file, change line 100 to ** -v $PYTHONIAN_CODE:/code \ **

4. Run the companions starting script from the terminal using ./run-companions.sh. This will open the engine in the browser at the http://localhost:9100/smgr.html#

5. Click start session and run Interaction Manager

6. From a NEW terminal window, run docker exec -it companions python3 /code/wikidata_agent.py (if you're running into error saying wikidata agent not found: cp "wikidata_agent.py" ~/companions/pythonian/)

7. Wait until other tabs besides Status show up in browser

8. Press interaction-manager, load krf, then select the .krf file

**Running Queries**

1. In the commands tab, paste **(goalOfSolve ?s (ist-Information BOTEMt (hasEconomicValue SouthAfrica 2017 GDPPerCapita ?GDPPerCapita)))** and press enter. You can replace the country name, year, and property (GDP, GDPPerCapita) to match as needed

2. Recvd should be printed with a value in there SolveActivityFn X, where X is a number

3. Paste **(doRemoteAgentPlan session-reasoner (doRunToSolution (SolveActivityFn X)))** in Commands and run

4. Go back to status tab and wait until it goes from executing-plan to idle

**Viewing Query**

1. Right click on session reasoner and select graph solve tree. If everything worked, the top node should be green

2. To also view, right click on session reasoner and press browse WM. After a couple of seconds, in BOTEMt -> hasEconomicValue you can see everything you have proven.


**Example Queries**

1. Direct: (goalOfSolve ?s (ist-Information BOTEMt (hasEconomicValue UnitedStates 2015 GDP ?GDP)))
2. Decomposition: (goalOfSolve ?s (ist-Information BOTEMt (hasEconomicValue SouthAfrica 2017 GDPPerCapita ?GDPPerCapita)))
3. Analogical: (goalOfSolve ?s (ist-Information BOTEMt (hasEconomicValue Venezuela 2017 GDPPerCapita ?GDPPerCapita)))
4. Mereology: (goalOfSolve ?s (ist-Information BOTEMt (hasEconomicValue EuropeanUnion 2009 Population ?Pop)))
5. Unit Conversion: (goalOfSolve ?s (ist-Information BOTEMt (hasEconomicValueInUnit SouthAfrica 2017 GDPPerCapita ?value EUR)))


**Unit Conversion Queries**

Unit conversion uses a separate predicate `hasEconomicValueInUnit` that takes a target currency as a fifth argument. The system retrieves the base USD value (via direct lookup, decomposition, or analogical reasoning as needed), then converts using historical exchange rates from frankfurter.app.

Query format:
(goalOfSolve ?s (ist-Information BOTEMt (hasEconomicValueInUnit Country Year Property ?value CurrencyCode)))

Run it to solution the same way as any other query:
(doRemoteAgentPlan session-reasoner (doRunToSolution (SolveActivityFn X)))

To view results: right click session-reasoner -> browse WM -> BOTEMt -> hasEconomicValueInUnit

Supported currency codes include: EUR, GBP, TRY, JPY, CNY, BRL, INR, KRW, CAD, AUD (any currency supported by frankfurter.app). Exchange rates are historically accurate for the queried year.

Note: all existing hasEconomicValue queries continue to work unchanged and return values in USD.
