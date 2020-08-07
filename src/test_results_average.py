import simulation
import sys
import subprocess
import pytest
import os.path
from os import path
import csv
import numpy as np
from decimal import Decimal


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
    def teardown_class(self):
        os.remove(outfile)

    def test_print_running(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        results = subprocess.check_output([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])
        assert (results[0:153].decode("utf-8") == "Startup\nStarting openrocket\nRunning 5 sims\nRunning simulation  1\nRunning simulation  2\nRunning simulation  3\nRunning simulation  4\nRunning simulation  5\n")
    
    def test_average_latitude(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        results = subprocess.check_output([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])
        
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            latTotal = 0
            count = 0
            for row in reader:
                count +=1
                try:
                    latTotal = latTotal + float(row["Latitude"])
                except ValueError:
                    assert False, "not a float" 
            latTotal = latTotal/count

            toCompare = Decimal(latTotal).quantize(Decimal("1.000"))
            assert (results[153:185].decode("utf-8") == "Rocket landing zone " + str(toCompare) + " lat, ")

    def test_average_longitude(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        results = subprocess.check_output([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])
        
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            longTotal = 0
            count = 0
            for row in reader:
                count +=1
                try:
                    longTotal = longTotal + float(row["Longitude"])
                except ValueError:
                    assert False, "not a float" 
            longTotal = longTotal/count
            toCompare = Decimal(longTotal).quantize(Decimal("1.000"))
            assert (results[185:197].decode("utf-8") == str(toCompare) + " long. ")

    def test_average_max_altitude(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        results = subprocess.check_output([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])
        
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            altTotal = 0
            count = 0
            for row in reader:
                count +=1
                try:
                    altTotal = altTotal + float(row["Max Altitude"])
                except ValueError:
                    assert False, "not a float" 
            altTotal = altTotal/count
            toCompare = Decimal(altTotal).quantize(Decimal("11.000"))
            assert (results[197:225].decode("utf-8") == "Max altitude " + str(toCompare) + " metres. ")

    def test_average_max_pos_upwind(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        results = subprocess.check_output([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])
        
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            upwindTotal = 0
            count = 0
            for row in reader:
                count +=1
                try:
                    upwindTotal = upwindTotal + float(row["Max Position upwind"])
                except ValueError:
                    assert False, "not a float" 
            upwindTotal = upwindTotal/count
            toCompare = Decimal(upwindTotal).quantize(Decimal("11.000"))
            assert (results[225:260].decode("utf-8") == "Max position upwind " + str(toCompare) + " metres. ")

    def test_average_max_pos_parallel(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        results = subprocess.check_output([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])
        
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            parallelTotal = 0
            count = 0
            for row in reader:
                count +=1
                try:
                    parallelTotal = parallelTotal + float(row["Max Position parallel to wind"])
                except ValueError:
                    assert False, "not a float" 
            parallelTotal = parallelTotal/count
            toCompare = Decimal(parallelTotal).quantize(Decimal("11.000"))
            assert (results[260:304].decode("utf-8") == "Max position parallel to wind " + str(toCompare) + " metres. ")

    def test_average_lateral_distance(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        results = subprocess.check_output([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])
        
        with open(outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            lateralTotal = 0
            count = 0
            for row in reader:
                count +=1
                try:
                    lateralTotal = lateralTotal + float(row["Lateral Distance (meters)"])
                except ValueError:
                    assert False, "not a float" 
            lateralTotal = lateralTotal/count
            toCompare = Decimal(lateralTotal).quantize(Decimal("11.000"))
            assert (results[304:347].decode("utf-8") == "Lateral distance " + str(toCompare) + " meters from start. ")