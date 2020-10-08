import sys
import subprocess
import pytest
import os.path
from os import path
import csv
from argparse import Namespace
from upwind_rocket_vectors import UpwindRocketVectors

args = Namespace(rocket='model.ork', outfile='./urv_tests.csv', rodAngle=45, rodAngleSigma=5, 
                rodDirection=0, rodDirectionSigma=5,
                windSpeed=15,windSpeedSigma=5, 
                startLat=0,startLong=0, simCount=1, 
                windDirection=0, motorPerformance = 0.1, parachute = 0,
                pValue=0.007,iValue=0.2,finName = "CONTROL")

class TestSim:

    # Test basic command line input
    def test_basic_input(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        upwind_args = Namespace(upwindStepSize=10, upwindMaxAngle=10, upwindMinAngle=-10)    
        urv = UpwindRocketVectors()
        urv.set_args(args,upwind_args)
        
        assert (urv.get_args() == args)
        returned_upwind_args = urv.get_upwind_args()
        assert (returned_upwind_args.upwindStepSize == 10)
        assert (returned_upwind_args.upwindMaxAngle == 10)
        assert (returned_upwind_args.upwindMinAngle == -10)
        
    # Test a negative step step size converts to positive
    def test_negative_step_input(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        upwind_args = Namespace(upwindStepSize=-10, upwindMaxAngle=10, upwindMinAngle=-10)    
        urv = UpwindRocketVectors()
        urv.set_args(args,upwind_args)
        
        assert (urv.get_args() == args)
        returned_upwind_args = urv.get_upwind_args()
        assert (returned_upwind_args.upwindStepSize == 10)
        assert (returned_upwind_args.upwindMaxAngle == 10)
        assert (returned_upwind_args.upwindMinAngle == -10)

    # Test negative angles convert to positive
    def test_reversed_angles_input(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        upwind_args = Namespace(upwindStepSize=15, upwindMaxAngle=-5, upwindMinAngle=5)    
        urv = UpwindRocketVectors()
        urv.set_args(args,upwind_args)
        
        assert (urv.get_args() == args)
        returned_upwind_args = urv.get_upwind_args()
        assert (returned_upwind_args.upwindStepSize == 15)
        assert (returned_upwind_args.upwindMaxAngle == 5)
        assert (returned_upwind_args.upwindMinAngle == -5)

    # Test the output is a valid angle
    def test_output_valid_angle(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        upwind_args = Namespace(upwindStepSize=10, upwindMaxAngle=10, upwindMinAngle=-10)     
        urv = UpwindRocketVectors()
        urv.set_args(args,upwind_args)
        urv.run_analysis()


        assert (urv.get_bestAngle() <= 10 ) 
        assert (urv.get_bestAngle() >= -10) 
        

    # Test the outpout of the best distance is positive
    def test_output_positive(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        upwind_args = Namespace(upwindStepSize=10, upwindMaxAngle=10, upwindMinAngle=-10)     
        urv = UpwindRocketVectors()
        urv.set_args(args,upwind_args)
        urv.run_analysis()


        assert (float(urv.get_bestDistance()) >= 0 )

    # Test the output is of size 3 
    def test_output_array_size(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        upwind_args = Namespace(upwindStepSize=10, upwindMaxAngle=10, upwindMinAngle=-10)     
        urv = UpwindRocketVectors()
        urv.set_args(args,upwind_args)
        urv.run_analysis()

        assert (len(urv.get_distance_array()) == 3)

    # Test the output is the smalles option. 
    def test_output_smallest_option(self):
        try:
            from unittest.mock import patch
        except ImportError:
            from mock import patch

        upwind_args = Namespace(upwindStepSize=10, upwindMaxAngle=10, upwindMinAngle=-10)     
        urv = UpwindRocketVectors()
        urv.set_args(args,upwind_args)
        urv.run_analysis()

        assert (min(urv.get_distance_array()) == urv.get_bestDistance())
