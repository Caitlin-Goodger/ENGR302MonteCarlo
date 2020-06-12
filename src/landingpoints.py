import abstractlistener
import orhelper
import math
from jpype import *
from random import gauss
import csv
import numpy as np
from argparse import Namespace

class LandingPoints():
    "A list of landing points with ability to run simulations and populate itself"    
    
    def __init__(self, args) :
        self.landing_points = []
        self.max_altitudes = []
        self.upwind = []
        self.parallel = []
        self.lateral_movement = []
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
                
                opts.setLaunchRodAngle(math.radians( gauss(self.args.rodangle, self.args.rodanglesigma) ))
                opts.setLaunchRodDirection(math.radians( gauss(self.args.roddirection, self.args.roddirectionsigma) ))
                opts.setWindSpeedAverage( gauss(self.args.windspeed, self.args.windspeedsigma) )
                for component_name in ('Nose cone', 'Body tube'):
                    component = orh.get_component_named( rocket, component_name )
                    mass = component.getMass()
                    component.setMassOverridden(True)
                    component.setOverrideMass( mass * gauss(1.0, 0.05) )
                
                ma = MaxAltitude()
                lp = LandingPoint()
                pu = PositionUpwind()
                pp = PositionParallel()
                lm = LateralMovement()
                orh.run_simulation(sim, [lp, ma, pu, pp, lm])
                self.landing_points.append( lp )
                self.max_altitudes.append( ma )
                self.upwind.append( pu )
                self.parallel.append ( pp )
                self.lateral_movement.append( lm )

    def print_stats(self):
        lats = [p.lat for p in self.landing_points]
        longs = [p.long for p in self.landing_points]
        altitudes = [p.max_height for p in self.max_altitudes]
        upwinds = [p.upwind for p in self.upwind]
        parallels = [p.parallel for p in self.parallel]
        lateral_directions = [p.lateral_direction for p in self.lateral_movement]
        lateral_distances = [p.lateral_distance for p in self.lateral_movement]

        with open(self.args.outfile, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Latitude","Longitude","Max Altitude", "Max Position upwind", "Max Position parallel to wind", "Lateral Distance", "Lateral Direction"])           
            for p, q, r , s, t, u, v in zip(lats, longs, altitudes, upwinds, parallels, lateral_directions, lateral_distances):
                writer.writerow([np.format_float_positional(p), np.format_float_positional(q), np.format_float_positional(r), np.format_float_positional(s), np.format_float_positional(t), np.format_float_positional(u), np.format_float_positional(v)])

        print ('Rocket landing zone %3.3f lat, %3.3f long. Max altitude %3.3f metres. Max position upwind %3.3f metres. Max position parallel to wind %3.3f metres. Lateral distance %3.3f meters. Lateral direction %3.3f degrees. Based on %i simulations.' % \
        (np.mean(lats), np.mean(longs), np.mean(altitudes), np.mean(upwinds), np.mean(parallels), np.mean(lateral_distances), np.mean(lateral_directions), len(self.landing_points) ))

    def getResults(self):
        lats = [p.lat for p in self.landing_points]
        longs = [p.long for p in self.landing_points]
        altitudes = [p.max_height for p in self.max_altitudes]
        upwinds = [p.upwind for p in self.upwind]
        parallels = [p.parallel for p in self.parallel]
        lateral_directions = [p.lateral_direction for p in self.lateral_movement]
        lateral_distances = [p.lateral_distance for p in self.lateral_movement]

        toReturn = Namespace(lat = np.mean(lats), long = np.mean(longs), altitude = np.mean(altitudes), upwind = np.mean(upwinds), parallel = np.mean(parallels), lateraldistance = np.mean(lateral_distances), lateraldirection = np.mean(lateral_directions), sims = len(self.landing_points) )
        return toReturn

class LandingPoint(abstractlistener.AbstractSimulationListener):
    def endSimulation(self, status, simulation_exception):      
        worldpos = status.getRocketPosition()
        conditions = status.getSimulationConditions()
        launchpos = conditions.getLaunchSite()
        geodetic_computation = conditions.getGeodeticComputation()
        landing_zone = geodetic_computation.addCoordinate(launchpos, worldpos)
        self.lat = float(landing_zone.getLatitudeDeg())
        self.long = float(landing_zone.getLongitudeDeg())

    def startSimulation(self, status):
        self.maxAlt=-1
    
    def postStep(self, status):
        self.maxAlt = max(self.maxAlt, float(status.getRocketPosition().z))

class MaxAltitude(abstractlistener.AbstractSimulationListener):
   
   def __init__(self) :
        self.max_height = 0

   def postStep(self, status):      
        self.max_height = float(max(self.max_height, status.getRocketPosition().z))

class PositionUpwind(abstractlistener.AbstractSimulationListener):
    def __init__(self) :
        self.upwind = 0

    def endSimulation(self, status, simulation_exception):
        upwindArrayList = status.getFlightData().get(JClass("net.sf.openrocket.simulation.FlightDataType").TYPE_POSITION_X)
        upwindArray = [] 
        for u in upwindArrayList:
            upwindArray.append(float(u))
        
        self.upwind = max(upwindArray)

class PositionParallel(abstractlistener.AbstractSimulationListener):
    def __init__(self) :
        self.parallel = 0

    def endSimulation(self, status, simulation_exception):
        parallelArrayList = status.getFlightData().get(JClass("net.sf.openrocket.simulation.FlightDataType").TYPE_POSITION_Y)
        parallelArray = [] 
        for p in parallelArrayList:
            parallelArray.append(float(p))
        
        self.parallel = max(parallelArray)

class LateralMovement(abstractlistener.AbstractSimulationListener):
   
   def __init__(self) :
        self.lateral_distance = 0
        self.lateral_direction = 0

   def endSimulation(self, status, simulation_exception):       
        #Lateral Distance
        self.lateral_distance = float(status.getFlightData().getLast(JClass("net.sf.openrocket.simulation.FlightDataType").TYPE_POSITION_XY))

        #Lateral Direction
        self.lateral_direction = float(status.getFlightData().getLast(JClass("net.sf.openrocket.simulation.FlightDataType").TYPE_POSITION_DIRECTION))