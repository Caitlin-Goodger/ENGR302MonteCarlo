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