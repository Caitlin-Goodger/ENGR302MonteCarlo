import simulation
import sys
import pytest

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
        assert sim.args.outfile == "./out.csv" and sim.args.rocket == "model.ork" and sim.args.simcount == 20

# Test the user is given overview on available parameters
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
