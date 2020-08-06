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
        #assert sim.args.rocket == sim.resource_path(guiMock.filename)
        assert sim.args.simCount == int(guiMock.n.get())
        assert sim.args.rodAngle == float(guiMock.rodAngle.get())
        assert sim.args.rodAngleSigma == float(guiMock.rodAngleSigma.get())
        assert sim.args.rodDirection == float(guiMock.rodDirection.get())
        assert sim.args.rodDirectionSigma == float(guiMock.rodDirectionSigma.get())
        assert sim.args.windSpeed == float(guiMock.windSpeed.get())
        assert sim.args.windSpeedSigma == float(guiMock.windSpeedSigma.get())
        assert sim.args.startLat == float(guiMock.lat.get())
        assert sim.args.startLong == float(guiMock.longa.get())


    # #Test that given differing parameters, the final args are changed to the correct type and value
    # def testChangedArgs(self):
    #     with mock.patch.object(gui.InputOptions, '__init__', return_value= None):
    #         mockGui = gui.MonteCarloApp()
    #         # assert MockClass1 is gui.MonteCarloApp
    #         # assert mockGui.MonteCarloApp.called

    #         # #Add defaults to mock
    #         #mockGui.args = Namespace(rocket='model.ork', outfile='./out.csv')

    #         #Change every input value
    #         # mockGui.frame.rodAngleEntry.set('50')
    #         mockGui.filename = 'model.orq'
    #         mockGui.outfile = './out.csv'
    #         mockGui.rodAngleEntry = tk.StringVar()
    #         #mockGui.rodAngle = tk.Entry(self,width=25,textvariable=mockGui.latEntry)
    #         # mockGui.rodAngleEntry.set("45")
            
    #         # #mockGui.get.side_effect = self.updateArgs
    #         mockGui.updateArgs(mockGui)
    #         # #assert mockGui.args == Namespace(rocket='model.orq', outfile='./out.csv')
    #         # mock_sim_set_args.assert_called_once()



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