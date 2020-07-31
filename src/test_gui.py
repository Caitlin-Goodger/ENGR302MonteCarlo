import simulation
import sys
import pytest
import gui
from unittest.mock import patch


# Test system defaults 
#@patch('gui.MonteCarloApp')
def test():
    guiMock = gui.MonteCarloApp()
    # try:
    #     from unittest.mock import patch
    # except ImportError:
    #     from mock import patch

    # with patch.object(sys, 'argv', testargs):  
    #     guiMock = gui.MonteCarloApp()
    assert(guiMock.frame.rodAngle.get() == '45')
    guiMock.frame.exec()
    
