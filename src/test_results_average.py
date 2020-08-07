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
            assert (results[153:183].decode("utf-8") == "Rocket landing zone " + str(toCompare) + " lat")

