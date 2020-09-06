class UpwindRocketVectors(object):
    def __init__(self) :
        self.args = 0
        self.upwind_args = 0
        self.bestAngle = 0
        self.bestDistance = -1

    def set_args(self,new_args,new_upwind_args) :
        self.args = new_args
        self.upwind_args = new_upwind_args
    
    def run_analysis(self):
        pass

        # currentAngle = self.args.minValue
        # while currentAngle < self.args.maxValue :
        #     print(currentAngle)
        #     currentAngle += self.args.stepValue

        # loop through
        # - start at first value
        # - while smaller than second value
        # - increment value: step
            # run num of monte carlo
            # check output distance
            # - average/max?
            # if smaller
            # - update bestAngle to currentAngle value
            # - update bestDistance to output distance value

    def get_args(self) :
        return self.args

    def get_upwind_args(self) :
        return self.upwind_args

    def get_bestAngle(self) :
        return self.bestAngle

    def get_bestDistance(self) :
        return self.bestDistance