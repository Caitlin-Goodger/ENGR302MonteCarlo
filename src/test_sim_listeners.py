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
    assert np.min(maxAlts) > 8
    assert np.max(maxAlts) < 32
    
def test_position_upwind():
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch
        
    maxPositionsUpwind=[]
    with open(outfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            maxPositionsUpwind.append(float(row["Max Position upwind"]))
    average = np.average(maxPositionsUpwind)
    print(average)
    assert average > 45
    assert average < 65
    assert np.min(maxPositionsUpwind) > 30
    assert np.max(maxPositionsUpwind) < 80

def test_position_parallel():
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch
        
    maxPositionsParallel=[]
    with open(outfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            maxPositionsParallel.append(float(row["Max Position parallel to wind"]))
    average = np.average(maxPositionsParallel)
    print(average)
    assert average >= 0
    assert average < 5
    assert np.min(maxPositionsParallel) >= 0
    assert np.max(maxPositionsParallel) < 15

def test_position_lateral_direction():
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch
        
    lateralMovement=[]
    with open(outfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lateralMovement.append(float(row["Lateral Direction"]))
    average = np.average(lateralMovement)
    print(average)
    assert average > 30
    assert average < 65
    assert np.min(lateralMovement) > 15
    assert np.max(lateralMovement) < 75
