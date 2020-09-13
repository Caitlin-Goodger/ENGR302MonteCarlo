import simulation 

class UpwindRocketVectors(object):
    def __init__(self) :
        self.args = 0
        self.upwind_args = 0
        self.bestAngle = 0
        self.bestDistance = -1
        self.distance_array = []
        
        self.sim = simulation.Simulation()
        # args = 0
        # self.sim.set_args(args)
        # self.sim.parse_args()


    def set_args(self,new_args,new_upwind_args) :
        self.args = new_args
        self.args.rodAngleSigma = 0
        
        self.upwind_args = new_upwind_args
        self.correct_order()
    
    def run_analysis(self):
        currentAngle = self.upwind_args.upwindMinAngle
        while currentAngle <= self.upwind_args.upwindMaxAngle :
            # update new value of rodAngle
            self.args.rodAngle = currentAngle

            # run simulation
            self.sim.set_args(self.args)
            simulationValue = self.sim.runSimulation()

            # get distance 
            distance = simulationValue.getResults().__dict__['lateraldistance']

            # update value if smaller
            if self.bestDistance == -1 or self.bestDistance > distance :
                self.bestDistance = distance
                self.bestAngle = currentAngle

            # store distances for possible use/testing
            self.distance_array.append(distance)

            currentAngle += self.upwind_args.upwindStepSize

    def correct_order(self) :
        if self.upwind_args.upwindStepSize < 0 : 
            self.upwind_args.upwindStepSize = self.upwind_args.upwindStepSize * -1
        
        if self.upwind_args.upwindMinAngle > self.upwind_args.upwindMaxAngle :
            minValue = self.upwind_args.upwindMaxAngle
            maxValue = self.upwind_args.upwindMinAngle

            self.upwind_args.upwindMinAngle = minValue
            self.upwind_args.upwindMaxAngle = maxValue

    def get_args(self) :
        return self.args

    def get_upwind_args(self) :
        return self.upwind_args

    def get_bestAngle(self) :
        return self.bestAngle

    def get_bestDistance(self) :
        return self.bestDistance

    def get_distance_array(self) :
        return self.distance_array