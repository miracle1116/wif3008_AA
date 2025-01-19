from controller import Robot, Motor, DistanceSensor

# Initialize the robot
robot = Robot()

# Get the ball and goal objects
ball = robot.getFromDef("BALL")
goal = robot.getFromDef("GOAL_BLUE")

# Set the robot's timestep
timeStep = robot.getBasicTimeStep()

# Goal line position (x-coordinate)
goal_line_x = 0.95  # x-position where the goal is considered scored

# Reset positions after scoring
initial_ball_position = [-0.3941671001829981, -0.2161906677467168, 0.029921519999999986]
initial_robot_position = [-0.3, 0.1, 0.05]

# Time step for the simulation
timeStep = robot.getBasicTimeStep()

# Get the e-puck motors
left_motor = robot.getDevice("left wheel")
right_motor = robot.getDevice("right wheel")

# Get the keyboard for manual control
keyboard = robot.getDevice("keyboard")
keyboard.enable(timeStep)  # Enable the keyboard to listen for events

# Set motors to velocity control mode
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# Main loop
while robot.step(timeStep) != -1:
    key = keyboard.getKey()
    
    # Default motor speed when no key is pressed
    left_motor_speed = 0.0
    right_motor_speed = 0.0

    # Control robot with keyboard
    if key == ord('W'):  # Move forward (W key)
        left_motor_speed = 2.0
        right_motor_speed = 2.0
    elif key == ord('S'):  # Move backward (S key)
        left_motor_speed = -2.0
        right_motor_speed = -2.0
    elif key == ord('A'):  # Turn left (A key)
        left_motor_speed = -1.5
        right_motor_speed = 1.5
    elif key == ord('D'):  # Turn right (D key)
        left_motor_speed = 1.5
        right_motor_speed = -1.5
    elif key == ord('Q'):  # Stop the robot (Q key)
        left_motor_speed = 0.0
        right_motor_speed = 0.0

    # Apply the speed to the motors
    left_motor.setVelocity(left_motor_speed)
    right_motor.setVelocity(right_motor_speed)
    # Get the ball's current position
    ball_position = ball.getPosition()  # (x, y, z)
    ball_x = ball_position[0]  # X-coordinate of the ball
    print(ball_x)

    # Check if the ball crosses the goal line
    if ball_x > goal_line_x:
        print("Goal!")
        # Stop the game (you could stop motors, reset ball and robot position)
        
        # Reset ball and robot to initial positions
        ball.setPosition(initial_ball_position)
        robot.setPosition(initial_robot_position)

        # You could also stop robot motion or trigger any other events here
        break  # Exit the loop if goal is scored
