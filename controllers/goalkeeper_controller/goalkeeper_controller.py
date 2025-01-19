from controller import Robot, Camera

TIME_STEP = 64

# Initialize the robot
robot = Robot()

# Devices
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
camera = robot.getDevice("camera")

# Enable devices
left_motor.setPosition(float('inf'))  # Enable velocity control
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0)  # Initially stationary
right_motor.setVelocity(0)
camera.enable(TIME_STEP)  # Enable the camera

# Movement parameters
goalkeeper_speed = 6.28  # Maximum wheel speed (rad/s)
goalkeeper_y_bounds = [-0.5, 0.5]  # Movement bounds along the y-axis

# Ball color detection thresholds
RED_MIN = 200
GREEN_MIN = 100
BLUE_MAX = 50

def detect_ball(camera, image, width, height):
    """
    Detect the ball in the camera image based on the color range.
    Returns the normalized y-coordinate of the ball's position.
    """
    for y in range(height):
        for x in range(width):
            red = camera.imageGetRed(image, width, x, y)
            green = camera.imageGetGreen(image, width, x, y)
            blue = camera.imageGetBlue(image, width, x, y)
            
            # Check if the pixel matches the ball's color
            if red > RED_MIN and green > GREEN_MIN and blue < BLUE_MAX:
                # Calculate the normalized y-coordinate (-1 to 1)
                return (2.0 * y / height) - 1.0
    return None  # Ball not found

while robot.step(TIME_STEP) != -1:
    # Get the camera image
    image = camera.getImage()
    width = camera.getWidth()
    height = camera.getHeight()

    if image:
        # Detect the ball
        ball_y = detect_ball(camera, image, width, height)

        if ball_y is not None:
            print(f"Ball detected at normalized y-coordinate: {ball_y}")

            # Map the ball's y-coordinate to the robot's movement bounds
            target_y = ball_y * (goalkeeper_y_bounds[1] - goalkeeper_y_bounds[0]) / 2

            # Move towards the target y position
            if target_y > 0.01:  # Move down (positive y)
                left_motor.setVelocity(goalkeeper_speed)
                right_motor.setVelocity(goalkeeper_speed)
            elif target_y < -0.01:  # Move up (negative y)
                left_motor.setVelocity(-goalkeeper_speed)
                right_motor.setVelocity(-goalkeeper_speed)
            else:
                # Stop if close enough to the target y position
                left_motor.setVelocity(0)
                right_motor.setVelocity(0)
        else:
            print("Ball not detected.")
            # Stop if the ball is not detected
            left_motor.setVelocity(0)
            right_motor.setVelocity(0)
    else:
        print("No image from the camera.")
