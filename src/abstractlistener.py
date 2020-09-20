class AbstractSimulationListener(object):
    """ This is a python implementation of openrocket.simulation.AbstractSimulationListener.
        Subclasses of this are suitable for passing to helper.run_simulation.
    """

    # The name of the proxy
    def __str__(self):
        return "'" + 'Python simulation listener proxy : ' + str(self.__class__.__name__) + "'"
    
    # The toString of the proxy
    def toString(self):
        return str(self)
    
    # Start Simulation Listener
    def startSimulation(self, status):
        pass
    
    # End Simulation Listener
    def endSimulation(self, status, simulation_exception):
        pass
    
    # Pre Step Simulation Listener
    def preStep(self, status):
        return True
         
    # Post Step Simulation Listener
    def postStep(self, status):
        pass
    
    # Listener for System
    def isSystemListener(self):
        return False
    
    # SimulationEventListener
    def addFlightEvent(self, status, flight_event):
        return True
    
    # Listener for handling flight events
    def handleFlightEvent(self, status, flight_event):
        return True
    
    # Listener deciding if the motor is ignited
    def motorIgnition(self, status, motor_id, motor_mount, motor_instance):
        return True
        
    # Listener deciding if the recovery device is depoloyed
    def recoveryDeviceDeployment(self, status, recovery_device):
        return True


class AbstractCompListener(AbstractSimulationListener):
    # Pre Acceleration Computation Listener
    def preAccelerationCalculation(self, status):
        return None
   
    # Pre Aerodynamic Computation Listener
    def preAerodynamicCalculation(self, status):
        return None
    
    # Pre Atmospheric Model Computation Listener
    def preAtmosphericModel(self, status):
        return None
    
    # Pre Flight Condition Computation Listener
    def preFlightConditions(self, status):
        return None
    
    # Pre Gravity Model Computation Listener
    def preGravityModel(self, status):
        return float('nan')
       
     # Pre Mass Calculation Listener
    def preMassCalculation(self, status):
        return None
        
    # Pre Simple thrust calculation Listener
    def preSimpleThrustCalculation(self, status):
        return float('nan')
    
    # Pre Wind Model computation Listener
    def preWindModel(self, status):
        return None
    
    # Post Acceleration calculation Listener
    def postAccelerationCalculation(self, status, acceleration_data):
        return None
    
    # Post Aerodynamic calculation Listener
    def postAerodynamicCalculation(self, status, aerodynamic_forces):
        return None
    
    # Post Atmospheric computation Listener
    def postAtmosphericModel(self, status, atmospheric_conditions):
        return None
    
    # Post flight condition Listener
    def postFlightConditions(self, status, flight_conditions):
        return None
        
    # Post Gravity model Listener
    def postGravityModel(self, status, gravity):
        return float('nan')
    
    # Post Mass Calculation Listener
    def postMassCalculation(self, status, mass_data):
        return None
    
    # Post Simple Thrust Calculation Listener
    def postSimpleThrustCalculation(self, status, thrust):
        return float('nan')
    
    # Post wind compution Listener
    def postWindModel(self, status, wind):
        return None