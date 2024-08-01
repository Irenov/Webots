from controller import Robot, Emitter

TIME_STEP = 64

# Initialize the robot
robot = Robot()

# Retrieve the central emitter
central_emitter = robot.getDevice('emitter')
central_emitter.setChannel(0)  # Set channel for the central emitter

def send_commands(channel, vx, vy, omega):
    command = f"{vx},{vy},{omega}"
    central_emitter.setChannel(channel)
    central_emitter.send(command.encode())

while robot.step(TIME_STEP) != -1:
    # Example movement commands
    send_commands(1, 1.0, 0.0, 0.0)  
    send_commands(2, 0.0, 1.0, 0.0)  
    send_commands(3, 0.0, 0.0, -1.0)
