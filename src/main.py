import numpy as np
from robot import Robot
from simulation import Simulation

def sixty_degree_line_path(robot, time):
    x_dot = 1
    y_dot = np.sqrt(3)
    v, w, z = robot.find_wheel_speeds(x_dot, y_dot, 0)
    return v, w, z

def circle_path(robot, time):
    x_dot = -np.sin(time)
    y_dot = np.cos(time)
    v, w, z = robot.find_wheel_speeds(x_dot, y_dot, 1)
    return v, w, z

def expanding_spiral_path(robot, time):
    x_dot = np.cos(time) - time * np.sin(time)
    y_dot = np.sin(time) + time * np.cos(time)
    v, w, z = robot.find_wheel_speeds(x_dot, y_dot, 1)
    return v, w, z

def main():
    # Create a robot object
    robot = Robot()
    
    # Create a simulation object
    sim = Simulation(robot)
    duration = 30
    dt = 0.1
    
    # Run the simulation
    #sim.run(-2, 1, 1, duration, window_size=[-10, 10])

    # for _ in range(int(duration/dt)):
    #     v, w, z = sixty_degree_line_path(robot, sim.time)
    #     sim.step(v, w, z, window_size=[-5, 55])

    # for _ in range(int(duration/dt)):
    #     v, w, z = circle_path(robot, sim.time)
    #     sim.step(v, w, z, window_size=[-3, 3])

    for _ in range(int(duration/dt)):
        v, w, z = expanding_spiral_path(robot, sim.time)
        sim.step(v, w, z, window_size=[-35, 35])
    
    sim.save()

if __name__ == '__main__':
    main()