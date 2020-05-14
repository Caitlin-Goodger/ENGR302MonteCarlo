import numpy as np
from jpype import *
import orhelper
from random import gauss
import math
import argparse
import csv

parser = argparse.ArgumentParser()
args = 0
        
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
            
            # Run num simulations and add to self
            for p in range(num):
                print ('Running simulation ', p)
                
                opts.setLaunchRodAngle(math.radians( gauss(args.rodangle, args.rodanglesigma) ))    # 45 +- 5 deg in direction
                opts.setLaunchRodDirection(math.radians( gauss(args.roddirection, args.roddirectionsigma) )) # 0 +- 5 deg in direction
                opts.setWindSpeedAverage( gauss(args.windspeed, args.roddirectionsigma) )                # 15 +- 5 m/s in wind
                for component_name in ('Nose cone', 'Body tube'):       # 5% in the mass of various components
                    component = orh.get_component_named( rocket, component_name )
                    mass = component.getMass()
                    component.setMassOverridden(True)
                    component.setOverrideMass( mass * gauss(1.0, 0.05) )
                
                airstarter = AirStart( gauss(1000, 50) ) # simulation listener to drop from 1000 m +- 50        
                lp = LandingPoint()
                orh.run_simulation(sim, [lp])
                self.append( lp )
    
    def print_stats(self):
        lats = [p.lat for p in self]
        longs = [p.long for p in self]
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
        
class AirStart(orhelper.AbstractSimulationListener):
    
    def __init__(self, altitude) :
        self.start_altitude = altitude
    
    def startSimulation(self, status) :        
        position = status.getRocketPosition()
        position = position.add(0.0, 0.0, self.start_altitude)
        status.setRocketPosition(position)

if __name__ == '__main__':

    parser.add_argument("-rocket", "--rocket", dest = "rocket", default = "model.ork", help="Model rocket file")
    parser.add_argument("-o", "--output", dest = "outfile", default = "./out.csv", help="Output CSV location")

    parser.add_argument("-rda", "--rodangle", dest = "rodangle", default = 45, help="Launch rod angle", type=float)
    parser.add_argument("-rdas", "--rodanglesigma", dest = "rodanglesigma", default = 5, help="Launch rod angle sigma", type=float)

    parser.add_argument("-rdd", "--roddirection", dest = "roddirection", default = 0, help="Launch rod direction", type=float)
    parser.add_argument("-rdds", "--roddirectionsigma", dest = "roddirectionsigma", default = 5, help="Launch rod direction sigma", type=float)

    parser.add_argument("-wsa", "--windspeed", dest = "windspeed", default = 15, help="Wind speed average", type=float)
    parser.add_argument("-wsas", "--windspeedsigma", dest = "roddirectionsigma", default = 5, help="Wind speed average sigma", type=float)
    args = parser.parse_args()

    points = LandingPoints()
    points.add_simulations(5)
    points.print_stats()
