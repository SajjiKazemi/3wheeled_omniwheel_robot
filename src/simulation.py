import matplotlib.pyplot as plt
import numpy as np

# Define the simulation environment for a three-wheeled omniwheel robot
class Simulation:
    def __init__(self, robot):
        self.robot = robot
        self.dt = 0.1
        self.time = 0
        self.history = []
        self.trajectory_fig = plt.figure()
        self.trajectory_ax = self.trajectory_fig.add_subplot(111)
        self.param_fig, self.param_axs = plt.subplots(3, 1, figsize=(8, 12))     
        self.is_run = False

    
    def step(self, v, w, z, window_size=[20, 20]):
        """
        Get the wheel rotation speeds for each wheel and pass
        them to the robot to update the pose.
        """
        self.robot.step(v, w, z, self.dt)
        self.time += self.dt
        self.history.append(self.robot.get_pose())
        if not self.is_run:
            self.plot(window_size)

    def run(self, v, w, z, duration, window_size):
        """
        Run the simulation for a given duration with the given
        rotation speeds for each wheel.
        """
        self.is_run = True
        for _ in range(int(duration / self.dt)):
            self.step(v, w, z, window_size)
            self.plot(window_size)
    
    def plot(self, window_size):
        axis_lower_lim = window_size[0]
        axis_upper_lim = window_size[1]
        self.trajectory_ax.cla()
        history = np.array(self.history)
        self.trajectory_ax.plot(history[:, 0], history[:, 1], linewidth=2, color='red')
        self.trajectory_ax.set_xlim(axis_lower_lim, axis_upper_lim)
        self.trajectory_ax.set_ylim(axis_lower_lim, axis_upper_lim)
        self.trajectory_ax.set_xlabel('x')
        self.trajectory_ax.set_ylabel('y')
        self.trajectory_ax.set_title('Robot Trajectory')
        self.trajectory_ax.legend(['Trajectory'])

        self.plot_params()
        self.plot_body()
        plt.draw()
        plt.pause(0.1)

    def plot_params(self):
        history = np.array(self.history)
        self.param_axs[0].cla()
        self.param_axs[0].plot(history[:, 0], linewidth=2, color='red')
        self.param_axs[0].set_ylabel('x')
        self.param_axs[0].set_title('Robot Pose')
        self.param_axs[0].legend(['x'])

        self.param_axs[1].cla()
        self.param_axs[1].plot(history[:, 1], linewidth=2, color='blue')
        self.param_axs[1].set_ylabel('y')
        self.param_axs[1].legend(['y'])

        self.param_axs[2].cla()
        self.param_axs[2].plot(history[:, 2], linewidth=2, color='green')
        self.param_axs[2].set_xlabel('Time  (in tenths of a second)')
        self.param_axs[2].set_ylabel('theta')
        self.param_axs[2].legend(['theta'])

    def plot_body(self):
        # Define the vertices of an equilateral triangle
        side_length = self.robot.wheel_distance
        height = np.sqrt(3) / 2 * side_length  # Height of the equilateral triangle
        # Vertices of the equilateral triangle
        centre = np.array([0, 0])
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
        transformed_centre = 10 * centre @ R.T + np.array([[self.robot.x, self.robot.y]])
        transformed_vertices = 10 * vertices @ R.T + np.array([[self.robot.x, self.robot.y]])

        # Close the triangle by adding the first vertex at the end
        triangle = np.vstack([transformed_vertices, transformed_vertices[0]])
        self.trajectory_ax.plot(transformed_centre[0,0], transformed_centre[0,1], 'ro')
        self.trajectory_ax.plot(triangle[:, 0], triangle[:, 1], 'bo-', linewidth=2) 
        self.trajectory_ax.fill(triangle[:, 0], triangle[:, 1], 'skyblue', alpha=0.5)
        self.trajectory_ax.grid(True)

    def save(self, filename='trajectory.png'):
        self.trajectory_fig.savefig(filename)
        self.param_fig.savefig('parameters.png')
        with open('trajectory.txt', 'w') as f:
            for pose in self.history:
                f.write(f'{pose[0]}\t{pose[1]}\t{pose[2]}\n')

    


