import numpy as np
from jpype import *
import orhelper
from random import gauss
import math
import argparse
import csv
import sys
    
class LandingPoints(list):
    "A list of landing points with ability to run simulations and populate itself"    
    
    def add_simulations(self, num):
        with orhelper.OpenRocketInstance('../lib/build/jar/openrocket.jar', log_level='ERROR'):
            
            # Load the document and get simulation
            orh = orhelper.Helper()
            doc = orh.load_doc(args.rocket)
            sim = doc.getSimulation(0)
            
            # Randomize various parameters
            opts = sim.getOptions()
            rocket = opts.getRocket()

            # Set latitude and longitude
            sim.getOptions().setLaunchLatitude(args.startlat)
            sim.getOptions().setLaunchLongitude(args.startlong)

            sim.getOptions().setLaunchRodAngle(math.pi/3)
            # Run num simulations and add to self
            for p in range(num):
                print ('Running simulation ', p+1)
                
                opts.setLaunchRodAngle(math.radians( gauss(args.rodangle, args.rodanglesigma) ))    # 45 +- 5 deg in direction
                opts.setLaunchRodDirection(math.radians( gauss(args.roddirection, args.roddirectionsigma) )) # 0 +- 5 deg in direction
                opts.setWindSpeedAverage( gauss(args.windspeed, args.roddirectionsigma) )                # 15 +- 5 m/s in wind
                for component_name in ('Nose cone', 'Body tube'):       # 5% in the mass of various components
                    component = orh.get_component_named( rocket, component_name )
                    mass = component.getMass()
                    component.setMassOverridden(True)
                    component.setOverrideMass( mass * gauss(1.0, 0.05) )
                
                ma = MaxAltitude()
                lp = LandingPoint()
                orh.run_simulation(sim, [lp, ma])
                self.append( lp )
    
    def print_stats(self):
        lats = [p.lat for p in self]
        longs = [p.long for p in self]
        # altitudes = [p.alt for worldpos in self]
        with open(args.outfile, 'w', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow(["Latitude","Longitude"])
            writer.writerows([[p.lat,p.long] for p in self])
        print ('Rocket landing zone %3.3f lat, %3.3f long . Based on %i simulations.' % \
        (np.mean(lats), np.mean(longs), len(self) ))

class LandingPoint(orhelper.AbstractSimulationListener):
    def endSimulation(self, status, simulation_exception):      
        worldpos = status.getRocketPosition()
        conditions = status.getSimulationConditions()
        launchpos = conditions.getLaunchSite()
        geodetic_computation = conditions.getGeodeticComputation()
        landing_zone = geodetic_computation.addCoordinate(launchpos, worldpos)
        self.lat = float(landing_zone.getLatitudeDeg())
        self.long = float(landing_zone.getLongitudeDeg())

class MaxAltitude(orhelper.AbstractSimulationListener):
   
   def __init__(self) :
        self.worldpos = 0

   def postStep(self, status):      
        self.worldpos = max(self.worldpos, status.getRocketPosition().z)

   def endSimulation(self, status, simulation_exception):
       print('Max altitude: ' + str(self.worldpos))
        
class AirStart(orhelper.AbstractSimulationListener):
    
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

parser = DefaultHelpParser(argparse.ArgumentParser())
args = 0

if __name__ == '__main__':

    parser.add_argument("-rocket", "--rocket", dest = "rocket", default = "model.ork", help="The model rocket file to run the simulation with.")
    parser.add_argument("-o", "--output", dest = "outfile", default = "./out.csv", help="The output CSV location.")

    parser.add_argument("-rda", "--rodangle", dest = "rodangle", default = 45, help="The rod angle to launch at.", type = float)
    parser.add_argument("-rdas", "--rodanglesigma", dest = "rodanglesigma", default = 5, help="The rod angle sigma to launch at.", type = float)

    parser.add_argument("-rdd", "--roddirection", dest = "roddirection", default = 0, help="The rod direction to launch at.", type = float)
    parser.add_argument("-rdds", "--roddirectionsigma", dest = "roddirectionsigma", default = 5, help="The rod direction sigma to launch at.", type = float)

    parser.add_argument("-wsa", "--windspeed", dest = "windspeed", default = 15, help="The average wind speed.", type = float)
    parser.add_argument("-wsas", "--windspeedsigma", dest = "roddirectionsigma", default = 5, help="The average wind speed sigma.", type = float)

    parser.add_argument("-lat", "--lat", dest = "startlat", default= 0, help = "The starting latitude for the simulation.",  type = float)
    parser.add_argument("-long", "--long", dest = "startlong", default= 0, help = "The starting longitude for the simulation.",  type = float)
    parser.add_argument("-n", "--n", dest = "simcount", default = 20, help = "The number of simulations to run.", type = int) 
    args = parser.parse_args()

    points = LandingPoints()
    points.add_simulations(args.simcount)
    points.print_stats()
