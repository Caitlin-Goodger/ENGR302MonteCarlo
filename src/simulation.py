import orhelper
import abstractlistener
import landingpoints
import argparse
import sys
import os
import csv
import pandas as pd
        
#Class for setting Rocking position for an Air Start          
class AirStart(abstractlistener.AbstractSimulationListener):
    
    #Initialise the start altitude to the altitude given
    def __init__(self, altitude) :
        self.start_altitude = altitude
    
    #Start the simulation by adding the starting altitude to the Rocket posistion
    def startSimulation(self, status) :        
        position = status.getRocketPosition()
        position = position.add(0.0, 0.0, self.start_altitude)
        status.setRocketPosition(position)


#Parser to read help  
class DefaultHelpParser(argparse.ArgumentParser):
    #Print help if there is an arror
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit()

#Class for reading in the weather data that has been provided
class WeatherData(object):
    #Read in weather data. It's a csv file
    def read_weather_data(self, name):
        df= pd.read_csv(name, sep=', ',header=None,engine='python')
        return df

#Simulation class for reading args and starting the simulations
class Simulation(object):
    #Initialise the args and the landing points
    def __init__(self) :
        self.args = 0
        self.points=landingpoints.LandingPoints(self.args)

    #Set the arguments with the arguments that have been provided by the user
    def set_args(self,new_args) :
        self.args = new_args
        self.points = landingpoints.LandingPoints(self.args)
        return self.points

    #Parse the arguments
    def parse_args(self) :
        parser = DefaultHelpParser(argparse.ArgumentParser())
        
        parser.add_argument("-rocket", "--rocket", dest = "rocket", default = self.resource_path("model.ork"), help="The model rocket file to run the simulation with.")
        parser.add_argument("-o", "--output", dest = "outfile", default = "./out.csv", help="The output CSV location.")

        parser.add_argument("-rda", "--rodangle", dest = "rodAngle", default = 45, help="The rod angle to launch at.", type = float)
        parser.add_argument("-rdas", "--rodanglesigma", dest = "rodAngleSigma", default = 5, help="The rod angle sigma to launch at.", type = float)

        parser.add_argument("-rdd", "--roddirection", dest = "rodDirection", default = 0, help="The rod direction to launch at.", type = float)
        parser.add_argument("-rdds", "--roddirectionsigma", dest = "rodDirectionSigma", default = 5, help="The rod direction sigma to launch at.", type = float)

        parser.add_argument("-wsa", "--windspeed", dest = "windSpeed", default = 15, help="The average wind speed.", type = float)
        parser.add_argument("-wsas", "--windspeedsigma", dest = "windSpeedSigma", default = 5, help="The average wind speed sigma.", type = float)
        parser.add_argument("-wd", "--winddirection", dest = "windDirection", default = 0, help="The wind direction.", type = float)

        parser.add_argument("-lat", "--lat", dest = "startLat", default= 0, help = "The starting latitude for the simulation.",  type = float)
        parser.add_argument("-long", "--long", dest = "startLong", default= 0, help = "The starting longitude for the simulation.",  type = float)
        parser.add_argument("-n", "--n", dest = "simCount", default = 20, help = "The number of simulations to run.", type = int) 
        parser.add_argument("-w", "--w", dest = "weathercsv", default = "", help = "Weather csv file")
        parser.add_argument("-mp", "--motor-performance", dest = "motorPerformance", default = "", help = "Variation of motor performance e.g. 0.1")
        parser.add_argument("-pf", "--parachute-failure", dest = "parachute", default = 0, help = "Number of sims to run with failure deployment", type = int)

        self.args = parser.parse_args()

        self.points = landingpoints.LandingPoints(self.args)
        return self.points

    #Run the simulations with the args provided
    def runSimulation(self):
        self.points.add_simulations(self.args.simCount)
        self.points.print_stats()
        return self.points

    #Get the resource path
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path,relative_path)
