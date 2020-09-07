import abstractlistener
import orhelper
import math
from jpype import *
from random import gauss, uniform
import csv
import numpy as np
from argparse import Namespace
import os
import sys
from decimal import Decimal

class LandingPoints():
    "A list of landing points with ability to run simulations and populate itself"    
    
    def __init__(self, args) :
        self.landing_points = []
        self.max_altitudes = []
        self.upwind = []
        self.parallel = []
        self.lateral_movement = []
        self.parachute_fail = []
        self.args = args

    def add_simulations(self, num):
        with orhelper.OpenRocketInstance('../lib/build/jar/OpenRocket.jar', log_level='ERROR'):

            # Load the document and get simulation
            orh = orhelper.Helper()

            doc = orh.load_doc(self.args.rocket)
            parachute_setting = doc.getRocket().getParachute().getDeployEvent().toString()
            # print(doc.getRocket().getParachute())
            # doc.getRocket().getParachute().setDeployEventCustom("never")
            # print(doc.getRocket().getParachute().getDeployEvent())

            parachuteFlag = false

            # Run num simulations and add to self
            print("Running {} sims".format(num))
            for p in range(num):
                print ('Running simulation ', p+1)

                sim = doc.getSimulation(0)
                # Randomize various parameters
                opts = sim.getOptions()
                rocket = opts.getRocket()
                
                if (p == (num - self.args.parachute)):
                    doc.getRocket().getParachute().setDeployEventCustom("never")
                    parachuteFlag = true

                # Set latitude and longitude
                sim.getOptions().setLaunchLatitude(self.args.startLat)
                sim.getOptions().setLaunchLongitude(self.args.startLong)

                sim.getOptions().setLaunchRodAngle(math.pi/3)
                
                opts.setLaunchRodAngle(math.radians( gauss(self.args.rodAngle, self.args.rodAngleSigma) ))
                opts.setLaunchRodDirection(math.radians( gauss(self.args.rodDirection, self.args.rodDirectionSigma) ))
                opts.setWindSpeedAverage( gauss(self.args.windSpeed, self.args.windSpeedSigma) )
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

                wd = WindListener(self.args.windDirection, self.args.windSpeed)
                mp = MotorPerformance(self.args.motorPerformance)

                orh.run_simulation(sim, [lp, ma, pu, pp, lm,wd,mp])
                self.landing_points.append( lp )
                self.max_altitudes.append( ma )
                self.upwind.append( pu )
                self.parallel.append ( pp )
                self.lateral_movement.append( lm )   
                self.parachute_fail.append (parachuteFlag)

    def print_stats(self):
        lats = [p.lat for p in self.landing_points]
        longs = [p.long for p in self.landing_points]
        altitudes = [p.max_height for p in self.max_altitudes]
        upwinds = [p.upwind for p in self.upwind]
        parallels = [p.parallel for p in self.parallel]
        lateral_directions = [p.lateral_direction for p in self.lateral_movement]
        lateral_distances = [p.lateral_distance for p in self.lateral_movement]
        
        if self.isWritable(self.args.outfile):
            with open(self.args.outfile, 'w',newline="\n") as file:
                writer = csv.writer(file)
                writer.writerow(["Latitude","Longitude","Max Altitude", "Max Position upwind", "Max Position parallel to wind", "Lateral Distance (meters)", "Lateral Direction (°)", "Parachute fail?"])           
                for p, q, r , s, t, u, v, f in zip(lats, longs, altitudes, upwinds, parallels, lateral_distances, lateral_directions, self.parachute_fail):
                    writer.writerow([np.format_float_positional(p), np.format_float_positional(q), np.format_float_positional(r), np.format_float_positional(s), np.format_float_positional(t), np.format_float_positional(u), np.format_float_positional(v), f])
            file.close()
        else:
            print("Warning: unable to write to file: "+ self.args.outfile)
        print ('Rocket landing zone %+3.3f lat, %+3.3f long. Max altitude %3.3f metres. Max position upwind %+3.3f metres. Max position parallel to wind %+3.3f metres. Lateral distance %+3.3f meters from start. Lateral direction %+3.3f degrees from from the start (relative to East). Based on %i simulations.' % \
        (float(format(np.mean(lats))), float(format(np.mean(longs))), float(format(np.mean(altitudes))), float(format(np.mean(upwinds))), float(format(np.mean(parallels))), float(format(np.mean(lateral_distances))), float(format(np.mean(lateral_directions))), len(self.landing_points)))
        


    def isWritable(self,path):
        try:
            fileTest = open( path, 'w' )
            fileTest.close()
        except IOError:
            return False
        return True

    def getResults(self):
        lats = [p.lat for p in self.landing_points]
        longs = [p.long for p in self.landing_points]
        altitudes = [p.max_height for p in self.max_altitudes]
        upwinds = [p.upwind for p in self.upwind]
        parallels = [p.parallel for p in self.parallel]
        lateral_directions = [p.lateral_direction for p in self.lateral_movement]
        lateral_distances = [p.lateral_distance for p in self.lateral_movement]

        toReturn = Namespace(lat = np.format_float_positional(np.mean(lats)), long = np.format_float_positional(np.mean(longs)), altitude = np.format_float_positional(np.mean(altitudes)), upwind = np.format_float_positional(np.mean(upwinds)), parallel = np.format_float_positional(np.mean(parallels)), lateraldistance = np.format_float_positional(np.mean(lateral_distances)), lateraldirection = np.format_float_positional(np.mean(lateral_directions)), sims = len(self.landing_points) )
        return toReturn

    def format(self, s):
        return (Decimal(float(s)).quantize(Decimal("11.000")))

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

class WindListener(abstractlistener.AbstractCompListener):
    def __init__(self, direction, speed):
        try:
            self.direction = float(direction)
            self.speed = float(speed)
        except ValueError:
            self.direction = 0
            self.speed = 0

    def preWindModel(self, status):
        self.windDirection = JClass("net.sf.openrocket.util.Coordinate")(self.speed * math.sin(self.direction), self.speed * math.cos(self.direction), 0)
        return self.windDirection
    
class MotorPerformance(abstractlistener.AbstractCompListener):

    def __init__(self, variation):
        try:
            f = float(variation)
            self.variation = uniform(1-f, 1+f)
        except ValueError:
            self.variation = 1.0
        
    
    def postSimpleThrustCalculation(self, status, thrust):
        f = float(thrust * self.variation)
        return f
