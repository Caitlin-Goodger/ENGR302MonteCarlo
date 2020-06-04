import simulation
import sys
import subprocess
import pytest
import os.path
from os import path
import csv
import numpy as np

"""
averge with in range (
    max alt >0 and valid
    longatude & latitude are valid (lateral distance)
    position upwind and position parallel are valid
)

Check results are outputted reasonably to csv. 

check all inputs are within defined % range (we provide sigma)
"""
outfile="./csv_made.csv"



def setup_module():
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch
    subprocess.call([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])

def teardown_module():
    os.remove(outfile)

def test_csv_made():
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch
    assert path.exists(outfile)


def test_max_altitude():
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch

    maxAlts=[]
    with open(outfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            maxAlts.append(float(row["Max Altitude"]))
    average = np.average(maxAlts)
    print(average)
    assert average > 12
    assert average < 25
    assert np.min(maxAlts) > 10
    assert np.max(maxAlts) < 30
    
    

