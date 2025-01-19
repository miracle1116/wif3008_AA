from controller import Robot, Camera, DistanceSensor

class AutonomousSoccerRobot:
    def __init__(self):
        self.robot = Robot()
        self.time_step = int(self.robot.getBasicTimeStep())

        # Motors
        self.left_motor = self.robot.getDevice('left wheel motor')
        self.right_motor = self.robot.getDevice('right wheel motor')

        # Enable infinite position mode and set initial velocity
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

        # Camera to detect ball
        self.camera = self.robot.getDevice('camera')
        self.camera.enable(self.time_step)

        # Distance sensor for collision avoidance
        self.front_sensor = self.robot.getDevice('ps7')  # Example distance sensor
        self.front_sensor.enable(self.time_step)

        # Define constants
        self.chase_speed = 6.28
        self.avoid_obstacle_speed = 2.0

    def run(self):
        while self.robot.step(self.time_step) != -1:
            # Capture ball position using the camera
            ball_position = self.get_ball_position()

            # If the ball is detected, move towards it
            if ball_position is not None:
                x_position, y_position = ball_position

                if abs(x_position) > 0.1:  # Ball is to the left or right
                    # Turn towards the ball
                    if x_position < 0:
                        self.left_motor.setVelocity(-3)
                        self.right_motor.setVelocity(3)
                    else:
                        self.left_motor.setVelocity(3)
                        self.right_motor.setVelocity(-3)
                else:
                    # Move straight towards the ball
                    self.left_motor.setVelocity(self.chase_speed)
                    self.right_motor.setVelocity(self.chase_speed)

            else:
                # If the ball is not detected, search for it
                self.left_motor.setVelocity(3)
                self.right_motor.setVelocity(-3)

    def get_ball_position(self):
        """
        Analyze the camera's image and detect the ball's position.
        This method returns the ball's position (x, y) in the camera's field of view.
        """
        image = self.camera.getImage()
        width = self.camera.getWidth()
        height = self.camera.getHeight()

        for x in range(width):
            for y in range(height):
                red = self.camera.imageGetRed(image, width, x, y)
                green = self.camera.imageGetGreen(image, width, x, y)
                blue = self.camera.imageGetBlue(image, width, x, y)

                # Assuming the ball is yellow; detect the yellow color
                if red > 200 and green > 100 and blue < 50:
                    normalized_x = (x - width / 2) / (width / 2)
                    normalized_y = (y - height / 2) / (height / 2)
                    return normalized_x, normalized_y

        return None


if __name__ == "__main__":
    robot = AutonomousSoccerRobot()
    robot.run()
