import matplotlib.pyplot as plt
import numpy as np

# Define the simulation environment for a three-wheeled omniwheel robot
class Simulation:
    def __init__(self, robot):
        self.robot = robot
        self.dt = 0.1
        self.time = 0
        self.history = []
    
    def step(self, v, w, z):
        """
        Get the wheel rotation speeds for each wheel and pass
        them to the robot to update the pose.
        """
        self.robot.step(v, w, z, self.dt)
        self.time += self.dt
        self.history.append(self.robot.get_pose())

    def run(self, v, w, z, duration):
        """
        Run the simulation for a given duration with the given
        rotation speeds for each wheel.
        """
        for _ in range(int(duration / self.dt)):
            self.step(v, w, z)
    
    def plot(self):
        history = np.array(self.history)
        plt.plot(history[:, 0], history[:, 1])
        plt.axis('equal')
        plt.show()


    


