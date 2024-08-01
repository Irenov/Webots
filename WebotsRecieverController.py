from controller import Robot, Receiver

TIME_STEP = 64

# Initialize the robot
robot = Robot()

left_wheel_motor = robot.getDevice('left wheel motor')
right_wheel_motor = robot.getDevice('right wheel motor')
receiver = robot.getDevice('receiver')
if receiver is None:
    raise ValueError("Device 'receiver' not found")

receiver.enable(TIME_STEP)

def process_message(message):
    try:
        parts = message.split(',')
        vx = float(parts[0].strip())
        vy = float(parts[1].strip())
        omega = float(parts[2].strip())
        return vx, vy, omega
    except (IndexError, ValueError) as e:
        print(f"Error processing message: {message}")
        print(f"Exception: {e}")
        return 0.0, 0.0, 0.0  
        
# Set the receiver channel
receiver.setChannel(1)

left_wheel_motor.setPosition(float('inf'))
right_wheel_motor.setPosition(float('inf'))

def set_wheel_velocities(vx, vy, omega):
    left_wheel_velocity = vx - vy - omega
    right_wheel_velocity = vx + vy + omega
    
    left_wheel_motor.setVelocity(left_wheel_velocity)
    right_wheel_motor.setVelocity(right_wheel_velocity)

while robot.step(TIME_STEP) != -1:
    if receiver.getQueueLength() > 0:
        message = receiver.getString()
        vx, vy, omega = process_message(message)
        set_wheel_velocities(vx, vy, omega)
        receiver.nextPacket()
