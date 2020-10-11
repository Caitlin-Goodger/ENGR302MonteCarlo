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

# A list of landing points with ability to run simulations and populate itself
class LandingPoints():
    
    # Initialise all arguments 
    def __init__(self, args) :
        self.landing_points = []
        self.max_altitudes = []
        self.upwind = []
        self.parallel = []
        self.lateral_movement = []
        self.parachute_fail = []
        self.args = args

    # Add a simulation 
    def add_simulations(self, num):
        with orhelper.OpenRocketInstance('../lib/build/jar/OpenRocket.jar', log_level='ERROR'):

            # Load the document and get simulation
            orh = orhelper.Helper()

            doc = orh.load_doc(self.args.rocket)
            parachute_setting = doc.getRocket().getParachute().getDeployEvent().toString()
            parachuteFlag = False

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
                    parachuteFlag = True

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
                
                # Call computation listeners
                ma = MaxAltitude()
                lp = LandingPoint()
                pu = PositionUpwind()
                pp = PositionParallel()
                lm = LateralMovement()

                wd = WindListener(self.args.windDirection, self.args.windSpeed)
                mp = MotorPerformance(self.args.motorPerformance)

                rf = FinListener(self.args.pValue, self.args.iValue)
                orh.run_simulation(sim, [lp, ma, pu, pp, lm,wd,mp, rf])
                self.landing_points.append( lp )
                self.max_altitudes.append( ma )
                self.upwind.append( pu )
                self.parallel.append ( pp )
                self.lateral_movement.append( lm )   
                self.parachute_fail.append (parachuteFlag)

    # Print the results to the screen and out file
    def print_stats(self):
        lats = [p.lat for p in self.landing_points]
        longs = [p.long for p in self.landing_points]
        altitudes = [p.max_height for p in self.max_altitudes]
        upwinds = [p.upwind for p in self.upwind]
        parallels = [p.parallel for p in self.parallel]
        lateral_directions = [p.lateral_direction for p in self.lateral_movement]
        lateral_distances = [p.lateral_distance for p in self.lateral_movement]
        
        if self.isWritable(self.args.outfile):
            with open(self.args.outfile, 'w',newline="\n",encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Latitude","Longitude","Max Altitude", "Max Position upwind", "Max Position parallel to wind", "Lateral Distance (meters)", "Lateral Direction (°)", "Parachute failed"])           
                for p, q, r , s, t, u, v, f in zip(lats, longs, altitudes, upwinds, parallels, lateral_distances, lateral_directions, self.parachute_fail):
                    writer.writerow([np.format_float_positional(p), np.format_float_positional(q), np.format_float_positional(r), np.format_float_positional(s), np.format_float_positional(t), np.format_float_positional(u), np.format_float_positional(v), f])
            file.close()
        else:
            print("Warning: unable to write to file: "+ self.args.outfile)
        print ('Rocket landing zone %+3.3f lat, %+3.3f long. Max altitude %3.3f metres. Max position upwind %+3.3f metres. Max position parallel to wind %+3.3f metres. Lateral distance %+3.3f meters from start. Lateral direction %+3.3f degrees from the start (relative to East). Based on %i simulations.' % \
        (float(format(np.mean(lats))), float(format(np.mean(longs))), float(format(np.mean(altitudes))), float(format(np.mean(upwinds))), float(format(np.mean(parallels))), float(format(np.mean(lateral_distances))), float(format(np.mean(lateral_directions))), len(self.landing_points)))
        

    # Check if the test is writable
    def isWritable(self,path):
        try:
            fileTest = open( path, 'w' )
            fileTest.close()
        except IOError:
            return False
        return True

    # Gets the results and return them
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

    # Format a given float into a string
    def format(self, s):
        return (Decimal(float(s)).quantize(Decimal("11.000")))

# Computation listeners for landing points
class LandingPoint(abstractlistener.AbstractSimulationListener):
    # Defines the actions that should be completed at the end of a simulation
    # Sets the conditions and landing zone at the end of the simulation
    def endSimulation(self, status, simulation_exception):      
        worldpos = status.getRocketPosition()
        conditions = status.getSimulationConditions()
        launchpos = conditions.getLaunchSite()
        geodetic_computation = conditions.getGeodeticComputation()
        landing_zone = geodetic_computation.addCoordinate(launchpos, worldpos)
        self.lat = float(landing_zone.getLatitudeDeg())
        self.long = float(landing_zone.getLongitudeDeg())

    # Defines the actions that should be completed at the start of a simulation
    # Decreases the maximum altitude 
    def startSimulation(self, status):
        self.maxAlt=-1
    
    # Defines the actions that should be completed at the end of each step
    # Updates the maximum Altitude
    def postStep(self, status):
        self.maxAlt = max(self.maxAlt, float(status.getRocketPosition().z))

# Computation listeners for the maximum altitude 
class MaxAltitude(abstractlistener.AbstractSimulationListener):
   
   # Sets the max height to 0
   def __init__(self) :
        self.max_height = 0

    # Defines the actions that should be completed at the end of each step
    # Updates the maximum height
   def postStep(self, status):      
        self.max_height = float(max(self.max_height, status.getRocketPosition().z))

# Computation listeners for the upwind position
class PositionUpwind(abstractlistener.AbstractSimulationListener):
    #Set the upwind position to 0
    def __init__(self) :
        self.upwind = 0

    # Defines the actions that should be completed at the end of a simulation
    # Gets the direction upwind at the end of the simulation
    def endSimulation(self, status, simulation_exception):
        upwindArrayList = status.getFlightData().get(JClass("net.sf.openrocket.simulation.FlightDataType").TYPE_POSITION_X)
        upwindArray = [] 
        for u in upwindArrayList:
            upwindArray.append(float(u))
        
        self.upwind = max(upwindArray)

# Computation listeners for the parallel position
class PositionParallel(abstractlistener.AbstractSimulationListener):
    #Set the parallel position to 0
    def __init__(self) :
        self.parallel = 0

    # Defines the actions that should be completed at the end of a simulation
    # Gets the direction paralell at the end of the simulation
    def endSimulation(self, status, simulation_exception):
        parallelArrayList = status.getFlightData().get(JClass("net.sf.openrocket.simulation.FlightDataType").TYPE_POSITION_Y)
        parallelArray = [] 
        for p in parallelArrayList:
            parallelArray.append(float(p))
        
        self.parallel = max(parallelArray)

# Computation listeners for the lateral movement
class LateralMovement(abstractlistener.AbstractSimulationListener):
   
   # Sets the lateral distance and direcition to 0
   def __init__(self) :
        self.lateral_distance = 0
        self.lateral_direction = 0

    # Defines the actions that should be completed at the end of a simulation
    # Sets the lateral distance and direcition
   def endSimulation(self, status, simulation_exception):       
        #Lateral Distance
        self.lateral_distance = float(status.getFlightData().getLast(JClass("net.sf.openrocket.simulation.FlightDataType").TYPE_POSITION_XY))

        #Lateral Direction
        self.lateral_direction = float(status.getFlightData().getLast(JClass("net.sf.openrocket.simulation.FlightDataType").TYPE_POSITION_DIRECTION))

# Computation listeners for the wind 
class WindListener(abstractlistener.AbstractCompListener):
    # Set the direction and speed of the wind if available, and 0 otherwise
    def __init__(self, direction, speed):
        try:
            self.direction = float(direction)
            self.speed = float(speed)
        except ValueError:
            self.direction = 0
            self.speed = 0

    # Set the wind direction
    def preWindModel(self, status):
        self.windDirection = JClass("net.sf.openrocket.util.Coordinate")(self.speed * math.sin(self.direction), self.speed * math.cos(self.direction), 0)
        return self.windDirection

# Computation listeners for the motor performance    
class MotorPerformance(abstractlistener.AbstractCompListener):
    # Set the motor performance if available, and 1 otherwise
    def __init__(self, variation):
        try:
            f = float(variation)
            self.variation = uniform(1-f, 1+f)
        except ValueError:
            self.variation = 1.0
        
    # Set the motor performance
    def postSimpleThrustCalculation(self, status, thrust):
        f = float(thrust * self.variation)
        return f

# Computation listeners for the fins
class FinListener (abstractlistener.AbstractCompListener):

    # Initialise all relevent fin parameters
    def __init__(self, p, i):
        self.name = "CONTROL"
        self.desired_roll = 0.0
        self.desired_pitch = 0.0
        self.fin_turn_rate = 10 * math.pi / 180
        self.max_angle = 15 * math.pi / 180
        self.kP = p
        self.kI = i
        self.current_roll_rate = 0
        self.current_pitch_rate = 0
        self.prevTime = 0
        self.finpos = 0

    # Set the roll and pitch rate
    def postFlightConditions(self, status, flight_conditions):
        self.current_roll_rate = flight_conditions.getRollRate()
        self.current_pitch_rate = flight_conditions.getPitchRate()

    # Defines the actions that should be completed at the end of each step
    # Calculate the PID and adjust fin as required
    def postStep(self, status):
        fins = None
        for c in status.getConfiguration():
            if ("FinSet" in c.getClass().toString() and self.name == c.getName()):
                fins = c
                break
        
        if fins is None:
            return
        deltaT = status.getSimulationTime() - self.prevTime
        self.prevTime = status.getSimulationTime()

        error = self.desired_roll - self.current_roll_rate - self.current_pitch_rate

        p = self.kP * error
        i = self.kI * error

        value = p + i

        if abs(value) > self.max_angle:
            value = self.max_angle if value > self.max_angle else -self.max_angle
        
        if self.finpos < value:
            self.finpos = min(self.finpos + self.fin_turn_rate * deltaT,value)
        else:
            self.finpos = max(self.finpos - self.fin_turn_rate, value)
        
        fins.setCantAngle(self.finpos)