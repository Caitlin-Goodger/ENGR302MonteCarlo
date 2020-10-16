# Prereqs

- Python3
- Apache Ant
- Conda

# Running instructions


1. Clone the repo to a new directory
   <code>git clone REPOURL</code>

2. Package OpenRocket JAR
   <code>cd lib/openrocketjava/</code>
   <code>ant jar</code>

3. Create new conda environment
    <code> conda create --name NAME python=3.5 </code>

4. Install requirements
   <code> pip install -r requirements.txt </code>

5. Install JPype
   <code> conda install -c conda-forge jpype1 </code>

6. Run code
   <code> python gui.py </code>

7. Optionally run code with command line
   <code> python monte_carlo.py PARAMS </code>