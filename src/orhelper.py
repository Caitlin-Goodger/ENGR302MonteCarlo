import sys, traceback
from jpype import *
import numpy as np
import os

class OpenRocketInstance(object):
    """ When instantiated, this class starts up a new openrocket instance.
        This class is designed to be called using the 'with' construct. This
        will ensure that no matter what happens within that context, the 
        JVM will always be shutdown.
    """
    
    def __init__(self, jar_path, log_level='ERROR'):
        """ jar_path is the full path of the OpenRocket .jar file to use
            log_level can be either ERROR, WARN, USER, INFO, DEBUG or VBOSE
        """

        print("Startup")
            
        print("Using jar at {}".format(self.resource_path(jar_path)))
        print(os.path.exists(self.resource_path(jar_path)))
        startJVM(getDefaultJVMPath(), "-Djava.class.path=%s" % self.resource_path(jar_path), convertStrings=False)
 
        orp = JPackage("net").sf.openrocket
        orp.startup.Startup2.loadMotor()
    
    def __enter__(self):
        print ('Starting openrocket')
             
    def __exit__(self, ty, value, tb):
        
        shutdownJVM()
        
        if not ty is None:
            print ('Exception while calling openrocket')
            print ('Exception info : ', ty, value, tb)
            print ('Traceback : ',traceback.print_exception(ty, value, tb))
    
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, "openrocket.jar")
        
class Helper(object):
    """ This class contains a variety of useful helper functions and wrapper for using
        openrocket via jpype. These are intended to take care of some of the more
        cumbersome aspects of calling methods, or provide more 'pythonic' data structures
        for general use.
    """
    
    def __init__(self):
        self.orp = JPackage("net").sf.openrocket

    def load_doc(self, or_filename):
        """ Loads a .ork file and returns the corresponding openrocket document """
        or_java_file = java.io.File(or_filename)
        loader = self.orp.file.GeneralRocketLoader()
        doc = loader.load(or_java_file)
        return doc
            
    def run_simulation(self, sim, listeners=None ):
        """ This is a wrapper to the Simulation.simulate() for running a simulation
            The optional listeners parameter is a sequence of objects which extend orh.AbstractSimulationListener.
        """
                
        if listeners == None:
            # this method takes in a vararg of SimulationListeners, which is just a fancy way of passing in an array, so 
            # we have to pass in an array of length 0 ..
            listener_array = JArray(self.orp.simulation.listeners.AbstractSimulationListener, 1)(0)
        else:
            listener_array = [JProxy( ( self.orp.simulation.listeners.SimulationListener, 
                                        self.orp.simulation.listeners.SimulationEventListener,
                                        self.orp.simulation.listeners.SimulationComputationListener
                                        ) , inst=c) for c in listeners]

        sim.getOptions().randomizeSeed() # Need to do this otherwise exact same numbers will be generated for each identical run
        sim.simulate( listener_array )

    def get_timeseries(self, simulation, variables, branch_number = 0):
        """Gets a dictionary of timeseries data (as numpy arrays) from a simulation given variable names.
           First parameter is an openrocket simulation object.
           Second parameter is a sequence of strings representing the variable names according to default locale.
        """
        branch = simulation.getSimulatedData().getBranch(branch_number)
        output = dict()
        for v in variables:            
            try:
                data_type = filter( lambda x : x.getName() == unicode(v) , branch.getTypes() ) [0]
            except:
                continue
            
            #openrocket returns an array of Double objects rather than primatives to have to get the data out this way
            output[v] = np.array( [i.value for i in branch.get(data_type)] ) 
        
        return output

    def get_final_values(self, simulation, variables, branch_number = 0):
        
        branch = simulation.getSimulatedData().getBranch(branch_number)
        output = dict()
        for v in variables:            
            try:
                data_type = filter( lambda x : x.getName() == unicode(v) , branch.getTypes() ) [0]
            except:
                continue
            
            #openrocket returns an array of Double objects rather than primatives to have to get the data out this way
            output[v] = branch.get(data_type)[-1].value
        
        return output

    def get_events(self, simulation):
        """Returns a dictionary of all the flight events in a given simulation.
           Key is the name of the event and value is the time of the event.
        """
        branch = simulation.getSimulatedData().getBranch(0)
        
        output = dict()
        for ev in branch.getEvents():
            output[str(ev.getType().toString())] = ev.getTime()
        
        return output

    def get_component_named(self, root, name):
        """ Finds and returns the first rocket component with the given name.
            Requires a root RocketComponent, usually this will be a RocketComponent.rocket instance.
            Raises a ValueError if no component found.
        """
        
        for component in JIterator(root):
            if component.getName() == name:
                return component
        raise ValueError(root.toString()+' has no component named '+name)

    def get_Landing_Listener(self):
        return self.orp.simulation.listeners.Landing()

class JIterator(object):
    "This class is a wrapper for java iterators to allow them to be used as python iterators"
    
    def __init__(self, jit):
        "Give this any java object which implements iterable"
        self.jit = jit.iterator(True)
    
    def __iter__(self):
        return self
    
    def next(self):
        if not self.jit.hasNext():
            raise StopIteration()
        else:
            return self.jit.next()
    
    __next__ = next # Python 3.X compatibility     
