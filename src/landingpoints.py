import abstractlistener
import orhelper
import math
from random import gauss
import csv
import numpy as np

class LandingPoints(list):
    "A list of landing points with ability to run simulations and populate itself"    
    
    def __init__(self, args) :
        self.args = args

    def add_simulations(self, num):
        with orhelper.OpenRocketInstance('../lib/build/jar/openrocket.jar', log_level='ERROR'):
            
            # Load the document and get simulation
            orh = orhelper.Helper()
            doc = orh.load_doc(self.args.rocket)
            sim = doc.getSimulation(0)
            
            # Randomize various parameters
            opts = sim.getOptions()
            rocket = opts.getRocket()

            # Set latitude and longitude
            sim.getOptions().setLaunchLatitude(self.args.startlat)
            sim.getOptions().setLaunchLongitude(self.args.startlong)

            sim.getOptions().setLaunchRodAngle(math.pi/3)
            # Run num simulations and add to self
            for p in range(num):
                print ('Running simulation ', p+1)
                
                opts.setLaunchRodAngle(math.radians( gauss(self.args.rodangle, self.args.rodanglesigma) ))    # 45 +- 5 deg in direction
                opts.setLaunchRodDirection(math.radians( gauss(self.args.roddirection, self.args.roddirectionsigma) )) # 0 +- 5 deg in direction
                opts.setWindSpeedAverage( gauss(self.args.windspeed, self.args.roddirectionsigma) )                # 15 +- 5 m/s in wind
                for component_name in ('Nose cone', 'Body tube'):       # 5% in the mass of various components
                    component = orh.get_component_named( rocket, component_name )
                    mass = component.getMass()
                    component.setMassOverridden(True)
                    component.setOverrideMass( mass * gauss(1.0, 0.05) )
                
                lp = LandingPoint()
                orh.run_simulation(sim, [lp])
                self.append( lp )
    
    def print_stats(self):
        lats = [p.lat for p in self]
        longs = [p.long for p in self]
        with open(self.args.outfile, 'w', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow(["Latitude","Longitude"])
            writer.writerows([[p.lat,p.long] for p in self])
        print ('Rocket landing zone %3.3f lat, %3.3f long . Based on %i simulations.' % \
        (np.mean(lats), np.mean(longs), len(self) ))

    # args = self.args #

class LandingPoint(abstractlistener.AbstractSimulationListener):
    def endSimulation(self, status, simulation_exception):      
        worldpos = status.getRocketPosition()
        conditions = status.getSimulationConditions()
        launchpos = conditions.getLaunchSite()
        geodetic_computation = conditions.getGeodeticComputation()
        landing_zone = geodetic_computation.addCoordinate(launchpos, worldpos)
        self.lat = float(landing_zone.getLatitudeDeg())
        self.long = float(landing_zone.getLongitudeDeg())