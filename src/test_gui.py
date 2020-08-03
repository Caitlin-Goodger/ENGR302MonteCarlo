import simulation
import sys
import pytest
import gui
from unittest.mock import patch
import unittest
import unittest.mock as mock
from argparse import Namespace
import tkinter as tk 

def testChangedArgs():
    guiMock = gui.MonteCarloApp()
    # try:
    #     from unittest.mock import patch
    # except ImportError:
    #     from mock import patch

    # with patch.object(sys, 'argv', testargs):  
    #     guiMock = gui.MonteCarloApp()
    guiMock.frame.rodAngleEntry.set('50')
    print(guiMock.frame.rodAngle.get())
    guiMock.frame.updateArgs()

    sim = guiMock.frame.sim
    assert sim.args.outfile == guiMock.frame.outfile
    #assert sim.args.rocket == sim.resource_path(guiMock.frame.filename)
    assert sim.args.simCount == int(guiMock.frame.n.get())
    assert sim.args.rodAngle == float(guiMock.frame.rodAngle.get())
    assert sim.args.rodAngleSigma == float(guiMock.frame.rodAngleSigma.get())
    assert sim.args.rodDirection == float(guiMock.frame.rodDirection.get())
    assert sim.args.rodDirectionSigma == float(guiMock.frame.rodDirectionSigma.get())
    assert sim.args.windSpeed == float(guiMock.frame.windSpeed.get())
    assert sim.args.windSpeedSigma == float(guiMock.frame.windSpeedSigma.get())
    assert sim.args.startLat == float(guiMock.frame.lat.get())
    assert sim.args.startLong == float(guiMock.frame.longa.get())

# class TestGui:

    # @classmethod
    # def updateArgs(self, guiMock):
    #     guiMock.args = Namespace(rocket=guiMock.filename, outfile='./out.csv')

    # #Test that given differing parameters, the final args are changed to the correct type and value
    # @patch('gui.MonteCarloApp', autospec = True)
    # def testChangedArgs(self, MockClass1):
    #     with mock.patch('simulation.Simulation.set_args') as mock_sim_set_args:
    #         mockGui = gui.MonteCarloApp()
    #         assert MockClass1 is gui.MonteCarloApp
    #         assert gui.MonteCarloApp.called

    #         #Add defaults to mock
    #         mockGui.args = Namespace(rocket='model.ork', outfile='./out.csv')

    #         #Change every input value
    #         # mockGui.frame.rodAngleEntry.set('50')
    #         mockGui.filename = 'model.ork'
    #         mockGui.outfile = './out.csv'
    #         #mockGui.rodAngleEntry = tk.StringVar()
    #         #mockGui.rodAngle = tk.Entry(self,width=25,textvariable=mockGui.latEntry)
    #         # mockGui.rodAngleEntry.set("45")
            
    #         #mockGui.get.side_effect = self.updateArgs
    #         mockGui.updateArgs(mockGui)
    #         #assert mockGui.args == Namespace(rocket='model.orq', outfile='./out.csv')
    #         mock_sim_set_args.assert_called_once()



        #Check that the method to update the arguments in OR is called with the correct parameters
        # mockSimulation.set_args.assert_called_once()
        # mockGui.frame.exec.assert_called_once()
        # sim = mockGui.frame.sim
    #     assert sim.args.outfile == mock.frame.outfile
        # #assert sim.args.rocket == sim.resource_path(guiMock.frame.filename)
        # assert sim.args.simCount == int(guiMock.frame.n.get())
        # assert sim.args.rodAngle == float(guiMock.frame.rodAngle.get())
        # assert sim.args.rodAngleSigma == float(guiMock.frame.rodAngleSigma.get())
        # assert sim.args.rodDirection == float(guiMock.frame.rodDirection.get())
        # assert sim.args.rodDirectionSigma == float(guiMock.frame.rodDirectionSigma.get())
        # assert sim.args.windSpeed == float(guiMock.frame.windSpeed.get())
        # assert sim.args.windSpeedSigma == float(guiMock.frame.windSpeedSigma.get())
        # assert sim.args.startLat == float(guiMock.frame.lat.get())
        # assert sim.args.startLong == float(guiMock.frame.longa.get())

    # def testDefaultArgs():
    #     entry = mock.Mock()
    #         with mock.patch('myapp.gui.ports.set_widget_value') as set_widget_value:
    #             from myapp.gui.adaptors import EntryAdaptor
    #             adaptor = EntryAdaptor(entry)

    #             text = 'some user-typed text'
    #             adaptor.set_value(text)

    #             set_widget_value.assert_called_once_with(entry, text)

    # def testDefaultArgs():
    #     guiMock = gui.MonteCarloApp()
    #     guiMock.frame.rodAngleEntry.set('50')
    #     print(guiMock.frame.rodAngle.get())
    #     guiMock.frame.updateArgs()

    #     sim = guiMock.frame.sim
    #     guiMock.frame.focus_set()
    #     print(guiMock.frame.focus_get())
    #     assert sim.args.outfile == guiMock.frame.outfile
    #     assert sim.args.rocket == sim.resource_path(guiMock.frame.filename)
    #     assert sim.args.simCount == int(guiMock.frame.n.get())
    #     assert sim.args.rodAngle == float(guiMock.frame.rodAngle.get())
    #     assert sim.args.rodAngleSigma == float(guiMock.frame.rodAngleSigma.get())
    #     assert sim.args.rodDirection == float(guiMock.frame.rodDirection.get())
    #     assert sim.args.rodDirectionSigma == float(guiMock.frame.rodDirectionSigma.get())
    #     assert sim.args.windSpeed == float(guiMock.frame.windSpeed.get())
    #     assert sim.args.windSpeedSigma == float(guiMock.frame.windSpeedSigma.get())
    #     assert sim.args.startLat == float(guiMock.frame.lat.get())
    #     assert sim.args.startLong == float(guiMock.frame.longa.get())