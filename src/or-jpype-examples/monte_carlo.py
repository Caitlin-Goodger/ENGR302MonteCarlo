import numpy as np
from jpype import *
import numpy as np
import orhelper
from random import gauss
import math
        
class LandingPoints(list):
    "A list of landing points with ability to run simulations and populate itself"    
    
    def add_simulations(self, num):
        with orhelper.OpenRocketInstance('openrocket.jar', log_level='ERROR'):
            
            # Load the document and get simulation
            orh = orhelper.Helper()
            doc = orh.load_doc('model.ork')
            sim = doc.getSimulation(0)
            
            # Randomize various parameters
            opts = sim.getOptions()
            rocket = opts.getRocket()
            
            # Run num simulations and add to self
            for p in range(num):
                print 'Running simulation ', p
                
                opts.setLaunchRodAngle(math.radians( gauss(45, 5) ))    # 45 +- 5 deg in direction
                opts.setLaunchRodDirection(math.radians( gauss(0, 5) )) # 0 +- 5 deg in direction
                opts.setWindSpeedAverage( gauss(15, 5) )                # 15 +- 5 m/s in wind
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
        print 'Rocket landing zone %3.3f lat, %3.3f long . Based on %i simulations.' % \
            (np.mean(lats), np.mean(longs), len(self) )

class LandingPoint(orhelper.AbstractSimulationListener):
    def endSimulation(self, status, simulation_exception):      
        worldpos = status.getRocketPosition()
        conditions = status.getSimulationConditions()
        launchpos = conditions.getLaunchSite()
        geodetic_computation = conditions.getGeodeticComputation()
        landing_zone = geodetic_computation.addCoordinate(launchpos, worldpos)
        self.lat = landing_zone.getLatitudeDeg()
        self.long = landing_zone.getLongitudeDeg()
        
class AirStart(orhelper.AbstractSimulationListener):
    
    def __init__(self, altitude) :
        self.start_altitude = altitude
    
    def startSimulation(self, status) :        
        position = status.getRocketPosition()
        position = position.add(0.0, 0.0, self.start_altitude)
        status.setRocketPosition(position)

if __name__ == '__main__':
    points = LandingPoints()
    points.add_simulations(5)
    points.print_stats()
