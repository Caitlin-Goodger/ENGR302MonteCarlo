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
        output = results[0:153].decode("utf-8")
        assert ("Running simulation" in output)
    
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

            toCompare = '{0:+.3f}'.format(latTotal)
            output = results[153:184].decode("utf-8")
            assert ("Rocket landing zone" in output and toCompare in output)

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
            toCompare = '{0:+.3f}'.format(longTotal)
            output = results[185:197].decode("utf-8")
            assert ("long" in output and toCompare in output)

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
            toCompare = '{0:.3f}'.format(altTotal)
            output = results[198:226].decode("utf-8")
            assert ("Max altitude" in output and toCompare in output)

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
            toCompare = '{0:+.3f}'.format(upwindTotal)
            output = results[226:261].decode("utf-8")
            assert ("Max position upwind" in output and toCompare in output)

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
            toCompare = '{0:+.3f}'.format(parallelTotal)
            output = results[262:307].decode("utf-8")
            assert ("Max position parallel to wind" in output and toCompare in output)

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
            toCompare = '{0:+.3f}'.format(lateralTotal)
            output = results[307:350].decode("utf-8")
            assert (toCompare in output and "Lateral distance" in output)
    
    def test_average_lateral_direction(self):
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
                    lateralTotal = lateralTotal + float(row["Lateral Direction (°)"])
                except ValueError:
                    assert False, "not a float" 
            lateralTotal = lateralTotal/count
            toCompare = '{0:+.3f}'.format(lateralTotal)
            output = results[351:423].decode("utf-8")
            assert ("Lateral direction" in output and toCompare in output)
    
    def test_num_simulations(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch
        results = subprocess.check_output([sys.executable,'monte_carlo.py','--output', outfile,'--n','5'])
        output = results[424:447].decode("utf-8")
        assert ( "Based on 5 simulations" in output)