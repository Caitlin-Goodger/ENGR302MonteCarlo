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
outfile="csv_results.csv"

class TestSim:
    @classmethod
    def setup_class(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        subprocess.call([sys.executable,'monte_carlo.py','--output', outfile,'--n','5', '-pf', '2'])


    @classmethod
    def teardown_class(self):
        os.remove(outfile)

    def test_csv_made(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        assert path.exists(outfile)

    def test_csv_names(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            # row = reader.next()
            row = reader.fieldnames
            assert "Latitude" in row
            assert "Longitude" in row
            assert "Max Altitude" in row
            assert "Max Position parallel to wind" in row
            assert "Lateral Distance (meters)" in row
            assert "Lateral Direction (°)" in row
            assert "Parachute failed" in row
    
    def test_latitude(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                count +=1
                try:
                    float(row["Latitude"])
                except ValueError:
                    assert False, "not a float" 
            assert count == 5

    def test_longitude(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                count +=1
                try:
                    float(row["Longitude"])
                except ValueError:
                    assert False, "not a float" 
            assert count == 5

    def test_max_altitude(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                count +=1
                try:
                    float(row["Max Altitude"])
                except ValueError:
                    assert False, "not a float" 
            assert count == 5

    def test_max_position_upwind(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                count +=1
                try:
                    float(row["Max Position upwind"])
                except ValueError:
                    assert False, "not a float" 
            assert count == 5

    def test_max_position_parallel_to_wind(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                count +=1
                try:
                    float(row["Max Position parallel to wind"])
                except ValueError:
                    assert False, "not a float" 
            assert count == 5

    def test_lateral_distance_meters(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                count +=1
                try:
                    float(row["Lateral Distance (meters)"])
                except ValueError:
                    assert False, "not a float" 
            assert count == 5

    def test_lateral_distance_degrees(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                count +=1
                try:
                    float(row["Lateral Direction (°)"])
                except ValueError:
                    assert False, "not a float" 
            assert count == 5

    def test_parachute_failure_number(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            false = 0
            true = 0
            for row in reader:
                if row["Parachute failed"] in "False":
                    false += 1
                if row["Parachute failed"] in "True":
                    true += 1
            assert true == 2
            assert false == 3