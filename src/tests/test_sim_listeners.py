from src import simulation
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
outfile="csv_made.csv"

class TestSim:
    @classmethod
    def setup_class(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        subprocess.call([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])


    @classmethod
    def teardown_class(self):
        os.remove(outfile)

    def test_csv_made(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        assert path.exists(outfile)


    def test_max_altitude(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            maxAlts=[]
            for row in reader:
                maxAlts.append(float(row["Max Altitude"]))
        average = np.average(maxAlts)
        print(average)
        assert average > 12
        assert average < 25
        assert np.min(maxAlts) > 8
        assert np.max(maxAlts) < 32
        
    def test_position_upwind(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
            
        maxPositionsUpwind=[]
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                maxPositionsUpwind.append(float(row["Max Position upwind"]))
        average = np.average(maxPositionsUpwind)
        print(average)
        assert average > 45
        assert average < 70
        assert np.min(maxPositionsUpwind) > 28
        assert np.max(maxPositionsUpwind) < 85

    def test_position_parallel(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
            
        maxPositionsParallel=[]
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                maxPositionsParallel.append(float(row["Max Position parallel to wind"]))
        average = np.average(maxPositionsParallel)
        print(average)
        assert average >= 0
        assert average < 6
        assert np.min(maxPositionsParallel) >= 0
        assert np.max(maxPositionsParallel) < 16

    def test_lateral_direction(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
            
        lateralMovement=[]
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lateralMovement.append(float(row["Lateral Direction (°)"]))
        average = np.average(lateralMovement)
        print(average)
        assert average > 25
        assert average < 65
        assert np.min(lateralMovement) > 0
        assert np.max(lateralMovement) < 85

    def test_lateral_distance(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
            
        lateralDistance=[]
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lateralDistance.append(float(row["Lateral Distance (meters)"]))
        average = np.average(lateralDistance)
        print(average)
        assert average > -0.7
        assert average < 0.7
        assert np.min(lateralDistance) > -3.5
        assert np.max(lateralDistance) < 3.5
