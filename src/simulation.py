import matplotlib.pyplot as plt
import numpy as np

# Define the simulation environment for a three-wheeled omniwheel robot
class Simulation:
    def __init__(self, robot):
        self.robot = robot
        self.dt = 0.1
        self.time = 0
        self.history = []
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)

    
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
            self.plot()
    
    def plot(self):
        self.ax.cla()
        history = np.array(self.history)
        self.ax.plot(history[:, 0], history[:, 1])
        self.ax.axis('equal')
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Robot Trajectory')
        self.ax.legend(['Trajectory'])
        self.plot_body()
        #plt.show()
        plt.draw()
        plt.pause(0.1)

    def plot_body(self):
        # Define the vertices of an equilateral triangle
        side_length = self.robot.wheel_distance
        height = np.sqrt(3) / 2 * side_length  # Height of the equilateral triangle
        # Vertices of the equilateral triangle
        vertices = np.array([
            [-side_length/2, -height/3],  # First vertex at origin
            [side_length/2, -height/3],  # Second vertex
            [0, 2*height/3]  # Third vertex
        ])

        # Calculate transformed vertices
        theta = self.robot.theta
        R = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        transformed_vertices = 10 * vertices @ R.T + np.array([[self.robot.x, self.robot.y]])

        # Close the triangle by adding the first vertex at the end
        triangle = np.vstack([transformed_vertices, transformed_vertices[0]])
        self.ax.plot(triangle[:, 0], triangle[:, 1], 'bo-', linewidth=2) 
        self.ax.fill(triangle[:, 0], triangle[:, 1], 'skyblue', alpha=0.5)
        self.ax.grid(True)


    


