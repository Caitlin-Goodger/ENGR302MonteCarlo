from jpype import *
import orhelper
import abstractlistener
import landingpoints
import argparse
import sys
import os
        
class AirStart(abstractlistener.AbstractSimulationListener):
    
    def __init__(self, altitude) :
        self.start_altitude = altitude
    
    def startSimulation(self, status) :        
        position = status.getRocketPosition()
        position = position.add(0.0, 0.0, self.start_altitude)
        status.setRocketPosition(position)
    
class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit()


class Simulation(object):
    def __init__(self) :
        self.args = 0
        self.points=landingpoints.LandingPoints(self.args)

    def set_args(self,new_args) :
        self.args = new_args
        self.points = landingpoints.LandingPoints(self.args)
        return self.points

    def parse_args(self) :
        parser = DefaultHelpParser(argparse.ArgumentParser())
        
        parser.add_argument("-rocket", "--rocket", dest = "rocket", default = self.resource_path("model.ork"), help="The model rocket file to run the simulation with.")
        parser.add_argument("-o", "--output", dest = "outfile", default = "./out.csv", help="The output CSV location.")

        parser.add_argument("-rda", "--rodangle", dest = "rodangle", default = 45, help="The rod angle to launch at.", type = float)
        parser.add_argument("-rdas", "--rodanglesigma", dest = "rodanglesigma", default = 5, help="The rod angle sigma to launch at.", type = float)

        parser.add_argument("-rdd", "--roddirection", dest = "roddirection", default = 0, help="The rod direction to launch at.", type = float)
        parser.add_argument("-rdds", "--roddirectionsigma", dest = "roddirectionsigma", default = 5, help="The rod direction sigma to launch at.", type = float)

        parser.add_argument("-wsa", "--windspeed", dest = "windspeed", default = 15, help="The average wind speed.", type = float)
        parser.add_argument("-wsas", "--windspeedsigma", dest = "windspeedsigma", default = 5, help="The average wind speed sigma.", type = float)

        parser.add_argument("-lat", "--lat", dest = "startlat", default= 0, help = "The starting latitude for the simulation.",  type = float)
        parser.add_argument("-long", "--long", dest = "startlong", default= 0, help = "The starting longitude for the simulation.",  type = float)
        parser.add_argument("-n", "--n", dest = "simcount", default = 20, help = "The number of simulations to run.", type = int) 
        self.args = parser.parse_args()
        self.points = landingpoints.LandingPoints(self.args)
        return self.points

    def runSimulation(self):
        self.points.add_simulations(self.args.simcount)
        self.points.print_stats()
        return self.points

    
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path,relative_path)

    def runSimulation(self) :
        points = landingpoints.LandingPoints(self.args)
        points.add_simulations(self.args.simcount)
        points.print_stats()
