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


