class AbstractSimulationListener(object):
    """ This is a python implementation of openrocket.simulation.AbstractSimulationListener.
        Subclasses of this are suitable for passing to helper.run_simulation.
    """

    
    def __str__(self):
        return "'" + 'Python simulation listener proxy : ' + str(self.__class__.__name__) + "'"
    
    def toString(self):
        return str(self)
    
    # SimulationListener
    def startSimulation(self, status):
        pass
    
    def endSimulation(self, status, simulation_exception):
        pass
    
    def preStep(self, status):
        return True
        
    def postStep(self, status):
        pass
    
    def isSystemListener(self):
        return False
    
    # SimulationEventListener
    def addFlightEvent(self, status, flight_event):
        return True
    
    def handleFlightEvent(self, status, flight_event):
        return True
    
    def motorIgnition(self, status, motor_id, motor_mount, motor_instance):
        return True
        
    def recoveryDeviceDeployment(self, status, recovery_device):
        return True


class AbstractCompListener(AbstractSimulationListener):
    # SimulationComputationListener
    def preAccelerationCalculation(self, status):
        return None
    
    def preAerodynamicCalculation(self, status):
        return None
    
    def preAtmosphericModel(self, status):
        return None
    
    def preFlightConditions(self, status):
        return None
    
    def preGravityModel(self, status):
        return float('nan')
    
    def preMassCalculation(self, status):
        return None
        
    def preSimpleThrustCalculation(self, status):
        return float('nan')
        
    def preWindModel(self, status):
        return None
        
    def postAccelerationCalculation(self, status, acceleration_data):
        return None
        
    def postAerodynamicCalculation(self, status, aerodynamic_forces):
        return None
        
    def postAtmosphericModel(self, status, atmospheric_conditions):
        return None
    
    def postFlightConditions(self, status, flight_conditions):
        return None
    
    def postGravityModel(self, status, gravity):
        return float('nan')
    
    def postMassCalculation(self, status, mass_data):
        return None
    
    def postSimpleThrustCalculation(self, status, thrust):
        return float('nan')
    
    def postWindModel(self, status, wind):
        return None