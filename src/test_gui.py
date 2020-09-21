import simulation
import sys
import pytest
import gui
from unittest.mock import patch
import unittest
import unittest.mock as mock
from argparse import Namespace
import tkinter as tk 

class TestGui:

    def testDefaultArgs(self):
        guiMock = gui.InputOptions(None, None)
        guiMock.rodAngleEntry.set('50')
        print(guiMock.rodAngle.get())
        guiMock.updateArgs()

        sim = guiMock.sim
        
        assert sim.args.outfile == guiMock.outfile
        assert sim.args.simCount == int(guiMock.n.get())
        assert sim.args.rodAngle == float(guiMock.rodAngle.get())
        assert sim.args.rodAngleSigma == float(guiMock.rodAngleSigma.get())
        assert sim.args.rodDirection == float(guiMock.rodDirection.get())
        assert sim.args.rodDirectionSigma == float(guiMock.rodDirectionSigma.get())
        assert sim.args.windSpeed == float(guiMock.windSpeed.get())
        assert sim.args.windSpeedSigma == float(guiMock.windSpeedSigma.get())
        assert sim.args.startLat == float(guiMock.lat.get())
        assert sim.args.startLong == float(guiMock.longa.get())
