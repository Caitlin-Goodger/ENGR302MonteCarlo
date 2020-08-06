import simulation
import sys
import subprocess
import pytest
import os.path
from os import path
import csv
import numpy as np
import monte_carlo
    
outfile="csv_results.csv"

class TestResultAverages: 
   
    @classmethod
    def teardown_class(self):
        os.remove(outfile)

    def test_latitude_average(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        subprocess.call([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])
        #subprocess.check_output()

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

        
