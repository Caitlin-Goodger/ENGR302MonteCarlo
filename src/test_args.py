import simulation
import sys
import pytest
import re


# Test system defaults 
def test_no_params():
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch

    testargs = ["prog"]
    with patch.object(sys, 'argv', testargs):  
        sim = simulation.Simulation()
        args = 0
        sim.set_args(args)
        sim.parse_args()
        assert sim.args.outfile == "./out.csv" 
        assert sim.args.rocket == "model.ork" 
        assert sim.args.simcount == 20  
        assert sim.args.rodangle == 45 
        assert sim.args.rodanglesigma == 5 
        assert sim.args.roddirection == 0 
        assert sim.args.roddirectionsigma == 5
        assert sim.args.windspeed == 15
        assert sim.args.windspeedsigma == 5
        assert sim.args.startlat == 0
        assert sim.args.startlong == 0


# Test the user is given overview on available parameters when using help flag
def test_help(capsys):
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch

    testargs = ["prog","-h"]
    with patch.object(sys, 'argv', testargs):  
        with patch.object(sys, "exit"):
            sim = simulation.Simulation()
            args = 0
            sim.set_args(args)
            sim.parse_args()
            out = capsys.readouterr()
            assert "optional arguments:" in out.out

# Test the user is given overview on available parameters when using invalid flag
def test_invalid(capsys):
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch

    testargs = ["prog","-invalid"]
    with patch.object(sys, 'argv', testargs):  
        with patch.object(sys, "exit"):
            sim = simulation.Simulation()
            args = 0
            sim.set_args(args)
            sim.parse_args()
            out,err = capsys.readouterr()
            assert "optional arguments:" in out
            assert "error: unrecognized arguments" in err

# Test valid args are used
def test_valid_args(capsys):
    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch

    testargs = ["prog","-n", "5", "-lat", "60", "-long", "50", "-wsa", "1"]
    with patch.object(sys, 'argv', testargs):  
        with patch.object(sys, "exit"):
            sim = simulation.Simulation()
            args = 0
            sim.set_args(args)
            sim.parse_args()
            sim.runSimulation()
            out = capsys.readouterr()
            lat = "60.... lat"
            long = "50.... long"
            assert (re.search(lat,out.out) is not None)
            assert (re.search(long,out.out) is not None)
