# Performance Assessment 2 - Tri 2
Further support updates: 
- Upwind Rocket Vectors
	- This includes the logic and GUI capabilities to run this. 
- Parachute Failures
	-  This includes modification of both the Java and Python to add this capability.
	- This was an important extension, requested by our Client.
- Further Map display
	- Support for displaying Parachute failures on the Map was added.
	- Bug fixes for Mapping was added.
	- Merged into master, integrated into GUI.
- Further tests were added
	- This includes additional tests in the test suite, as well as manual testing (reflected in the manual testing document  on the Wiki).

Running instructions:
1. Checkout desired branch of repo (master)
2. cd group14/lib/openrocketjava
3. `ant jar`
4. cd ../../src
5. `python gui.py`


# Performance Assessment 1 - Tri 2
Further support updates: 
- Reworking GUI to support also include Linux and Mac (Prior only windows supported)
- Weather csv input for GUI parameters
- Moter performance and wind direction 
- - java and py side
Starting development for 
- Maps display
- Refactoring of tests
 
Instructions to run Maps
- Maps are currently not merged into master, so ensure that you are on the maps branch
1. Checkout desired branch of repo (maps)
2. cd group14/lib/openrocketjava
3. ant jar
4. cd ../../
5. pip install -r requirements.txt
6. cd ./src
7. python gui.py to run the simulations that you want to map. 
8. python maps.py

# Performance Assessment 2 

We are currently in the process of developing two seperate features:
- GUI
- Packaging into standalone executables.
 
GUI has been merged into master, to run this:
1. Checkout desired branch of repo (master)
2. cd group14/lib/openrocketjava
3. ant jar
4. cd ../../src
5. python gui.py

To run packaging, this currently only works on MacOS and Linux (not windows)
- Ensure you are on the correct python environment with Jpype, PyInstaller installed
1. cd group14/lib/openrocketjava/src
2. python -m PyInstaller monte_carlo.spec

To Run:
1. cd dist
2. ./monte_carlo

# Development build instructions

- Ensure you are on the correct python environment with Jpype installed

1. Checkout desired branch of repo (master, input-output-demo etc)
2. cd group14/lib/openrocketjava
3. ant jar
4. cd ../../src
5. python monte_carlo.py - {PARAMS} (use -h for help)

Debug steps:

- If the program runs but fails to init java instance, ensure your jar has been built to /group14/lib/build/jar/openrocket.jar