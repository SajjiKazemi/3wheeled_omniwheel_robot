import numpy as np

class Robot:
    def __init__(self, x=0, y=0, theta=0):
        self.x = x
        self.y = y
        self.theta = theta
        self.wheel_radius = 0.1         # Radius of the wheels in meters
        self.wheel_distance = 0.2       # Distance of wheel connectons to the centre of triangle in meters
        self.wheel_speeds = [0, 0, 0]
        self.H_matrix = (1/self.wheel_radius)*np.array([
            [-self.wheel_distance, 1, 0],
            [self.wheel_distance, -0.5, -np.sqrt(3)/2],
            [self.wheel_distance, -0.5, np.sqrt(3)/2]])
        self.H_inv = np.linalg.inv(self.H_matrix)
    
    def step(self, v, w, z, dt):
        """
        Update the robot's pose based on the wheel speeds.
        """
        self.theta_dot, self.x_dot, self.y_dot = np.dot(self.H_inv, [v, w, z])
        
        self.theta += self.theta_dot * dt
        self.x += self.x_dot * dt
        self.y += self.y_dot * dt
    
    def find_wheel_speeds(self, x_dot, y_dot, theta_dot):
        """
        Find the wheel speeds based on the robot's pose.
        """
        v, w, z = np.dot(self.H_matrix, [theta_dot, x_dot, y_dot])
        return v, w, z
    
    def get_pose(self):
        return self.x, self.y, self.theta