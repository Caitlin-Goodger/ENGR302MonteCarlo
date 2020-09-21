import simulation 
# Setup simulation with arguments from command line
args = 0
sim = simulation.Simulation()
sim.set_args(args)
sim.parse_args()
sim.runSimulation()
