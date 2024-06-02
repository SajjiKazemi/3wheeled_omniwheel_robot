import numpy as np
from robot import Robot
from simulation import Simulation

def main():
    # Create a robot object
    robot = Robot()
    
    # Create a simulation object
    sim = Simulation(robot)
    
    # Run the simulation
    sim.run(1, -1, 1, 10)
    
    # Plot the trajectory
    sim.plot()

if __name__ == '__main__':
    main()