# Instructions for Running Agent in Companions

1. Download the run-companions script, agent file, and .krf file

2. Make sure you have local directory *companions*. You may have to run the run-companions script once to generate all of the folders inside of it.

2. Place agent file into companions -> pythonian folder

3. Run the companions starting script from the terminal using ./run-companions.sh. This will open the engine in the browser at the http://localhost:9100/smgr.html#

4. Click start session and run Interaction Manager

5. From a NEW terminal window, run docker exec -it companions python3 /code/wikidata_agent.py (if you're running into error saying wikidata agent not found: cp "wikidata_agent.py" ~/companions/pythonian/)

6. Wait until other tabs besides Status show up in browser

7. Press interaction-manager, load krf, then select the .krf file

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
