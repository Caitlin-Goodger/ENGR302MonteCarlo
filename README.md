# Development build instructions

- Ensure you are on the correct python environment with Jpype installed

1. Checkout desired branch of repo (master, input-output-demo etc)
2. cd group14/lib/openrocketjava
3. ant jar
4. cd ../../src
5. python monte_carlo.py - {PARAMS} (use -h for help)

Debug steps:

- If the program runs but fails to init java instance, ensure your jar has been built to /group14/lib/build/jar/openrocket.jar