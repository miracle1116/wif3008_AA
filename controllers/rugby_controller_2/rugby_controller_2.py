from controller import Supervisor, Keyboard
from PIL import Image, ImageDraw, ImageFont

TIME_STEP = 64

# Create the supervisor instance
supervisor = Supervisor()

# Get the motors using getDevice
left_motor = supervisor.getDevice("left wheel motor")
right_motor = supervisor.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))  # Set position to infinity for continuous rotation
right_motor.setPosition(float('inf'))

# Enable the keyboard
keyboard = Keyboard()
keyboard.enable(TIME_STEP)

# Get the ball, goal, and signboard from the world by their DEF names
ball = supervisor.getFromDef("BALL")
goal_blue = supervisor.getFromDef("GOAL_BLUE")
goal_signboard = supervisor.getFromDef("GOAL_SIGNBOARD")

# Get the wall from the world by its DEF name
wall = supervisor.getFromDef("Wall")

# Set the speed at which the wall will move
move_speed = 0.02  # Adjust the speed as needed
direction = 1  # 1 for right, -1 for left
max_distance = 0.7  # Maximum distance the wall can move (right)
min_distance = - 0.7  # Minimum distance the wall can move (left)

# Initial positions
initial_robot_position = [-0.8, 0, 6.396199578842521e-05]
initial_ball_position = [0, 0, 0.05]

# Goal counter
goal_count = 0

# Timer setup
total_time = 120.0 # Total time in seconds
start_time = supervisor.getTime()
last_update_time = -1 

def update_end_texture(count):
    # Create an image with a red background
    img = Image.new('RGB', (512, 128), color=(255, 0, 0))  # Red background
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 56)  # Ensure 'arial.ttf' is available

    # Add the "End" and "Total Goals" text in white
    draw.text((20, 5), "       Time's up!.", fill=(255, 255, 255), font=font)  # White text
    draw.text((20, 65), f"     Total Goals: {count}", fill=(255, 255, 255), font=font)
    
    # Save the texture to file
    img_path = "textures/goal_signboard.png"
    img.save(img_path)
    
    # Save the image
    shape_node = goal_signboard.getField("children").getMFNode(0)  # Get the Shape node
    appearance_node = shape_node.getField("appearance").getSFNode()  # Get the Appearance node
    texture_node = appearance_node.getField("texture").getSFNode()  # Get the ImageTexture node
    url_field = texture_node.getField("url")  # Get the 'url' field of the ImageTexture node
    url_field.setMFString(0, "../controllers/rugby_controller_2/textures/temp.png")
    supervisor.step(1) 
    url_field.setMFString(0, "../controllers/rugby_controller_2/" +img_path)# Update the texture file path
    supervisor.step(1) 

def update_signboard_texture(count, remaining_time):
    # Create an image with the goal count
    img = Image.new('RGB', (512, 128), color=(255, 255, 255))  # White background
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 56)  # Ensure 'arial.ttf' is available
    draw.text((20, 20), f"      Goals:  {count}", fill=(0, 0, 0), font=font)  # Black text
    draw.text((20, 70), f"      Time: {remaining_time:.0f} s", fill=(0, 0, 0), font=font)
    
    # Save the texture to file
    img_path = "textures/goal_signboard.png"
    img.save(img_path)
    
    # Save the image
    shape_node = goal_signboard.getField("children").getMFNode(0)  # Get the Shape node
    appearance_node = shape_node.getField("appearance").getSFNode()  # Get the Appearance node
    texture_node = appearance_node.getField("texture").getSFNode()  # Get the ImageTexture node
    url_field = texture_node.getField("url")  # Get the 'url' field of the ImageTexture node
    url_field.setMFString(0, "../controllers/rugby_controller_2/textures/temp.png")
    supervisor.step(1) 
    url_field.setMFString(0, "../controllers/rugby_controller_2/" +img_path)# Update the texture file path
    supervisor.step(1) 
    
update_signboard_texture(goal_count, total_time)
ball.getField("translation").setSFVec3f(initial_ball_position)
supervisor.getSelf().getField("translation").setSFVec3f(initial_robot_position)

# Main control loop
while supervisor.step(TIME_STEP) != -1:
    # Calculate remaining time
    elapsed_time = supervisor.getTime() - start_time
    remaining_time = max(total_time - int(elapsed_time), 0)  # Convert to integer seconds
    
    # Update the signboard every second
    if int(elapsed_time) > last_update_time:
        last_update_time = int(elapsed_time)
        update_signboard_texture(goal_count, remaining_time)
    
    # End the simulation if time runs out
    if remaining_time <= 0:
        print("Time's up!")
        update_end_texture(goal_count)
        break
        
    # Read keyboard input
    key = keyboard.getKey()

    # Control the movement based on the key pressed
    if key == Keyboard.UP:  # Move forward
        left_motor.setVelocity(6.28)  # Set the motor speed (rad/s)
        right_motor.setVelocity(6.28)
    elif key == Keyboard.DOWN:  # Move backward
        left_motor.setVelocity(-6.28)
        right_motor.setVelocity(-6.28)
    elif key == Keyboard.LEFT:  # Turn left
        left_motor.setVelocity(-3)
        right_motor.setVelocity(3)
    elif key == Keyboard.RIGHT:  # Turn right
        left_motor.setVelocity(3)
        right_motor.setVelocity(-3)
    else:  # Stop movement if no key is pressed
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)

    # Get the current position of the ball
    ball_position = ball.getField("translation").getSFVec3f()

    # Check if the ball crosses the goal line (e.g., crosses the x=0.95 threshold)
    if ball_position[0] > 0.86:
        print('Goal !')
        goal_count += 1
        
        update_signboard_texture(goal_count, total_time)
        
        # Reset the ball to its initial position
        ball.getField("translation").setSFVec3f(initial_ball_position)
        #ball.getField("velocity").setSFVec3f([0, 0, 0])  # Stop the ball
        
        # Reset the robot to its initial position
        supervisor.getSelf().getField("translation").setSFVec3f(initial_robot_position)

        # Print goal message
        print(f"Goal! Total Goals: {goal_count}")
    
        # Get the current position of the wall
    current_translation = wall.getField("translation").getSFVec3f()
    
    # Move the wall up and down within the specified bounds (across the y-axis)
    new_y_position = current_translation[1] + direction * move_speed
    
    if new_y_position > max_distance:
        new_y_position = max_distance
        direction = -1  # Change direction to move down
    elif new_y_position < min_distance:
        new_y_position = min_distance
        direction = 1  # Change direction to move up
    
    # Update the translation of the wall
    wall.getField("translation").setSFVec3f([current_translation[0], new_y_position, current_translation[2]])