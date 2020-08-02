import simulation
import sys
import pytest
import gui
from unittest.mock import patch
import tkinter as tk 
import tkinter.ttk as ttk
import os


# import os
# if os.environ.get('DISPLAY','') == '':
#     print("no display")

# Test system defaults 
#@patch('gui.MonteCarloApp')
def testChangedArgs():
    print(os.environ)
    guiMock = gui.MonteCarloApp()
    # guiMock.withdraw()
    print(guiMock.frame.winfo_screen()) #withdraw()

    # guiMock.
    # tk.overrideredirect(True)
    # print(guiMock.frame.winfo_screen()) #withdraw()
    # guiMock.test()
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

# def testDefaultArgs():
#     guiMock = gui.MonteCarloApp()
#     # try:
#     #     from unittest.mock import patch
#     # except ImportError:
#     #     from mock import patch

#     # with patch.object(sys, 'argv', testargs):  
#     #     guiMock = gui.MonteCarloApp()
#     assert(guiMock.frame.rodAngle.get() == '45')
#     guiMock.frame.updateArgs()

#     with patch.object(sys, 'argv', testargs):  
#         sim = simulation.Simulation()
#         args = guiMock.frame.args
#         sim.set_args(args)
#         sim.parse_args()
#         assert sim.args.outfile == guiMock.frame.outfile
#         assert sim.args.rocket == sim.resource_path(guiMock.frame.filename)
#         assert sim.args.simCount == guiMock.frame.
#         assert sim.args.rodAngle == 45 
#         assert sim.args.rodAngleSigma == 5 
#         assert sim.args.rodDirection == 0 
#         assert sim.args.rodDirectionSigma == 5
#         assert sim.args.windSpeed == 15
#         assert sim.args.windSpeedSigma == 5
#         assert sim.args.startLat == 0
#         assert sim.args.startLong == 0