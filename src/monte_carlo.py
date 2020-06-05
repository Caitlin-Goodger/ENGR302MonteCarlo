import simulation 
import os
import sys
import glob

args = 0
sim = simulation.Simulation()
sim.set_args(args)
sim.parse_args()
sim.runSimulation()
