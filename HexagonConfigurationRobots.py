from controller import Robot

TIME_STEP = 64

class EPUCKController:
    def __init__(self):
        # Create an instance of the Robot
        self.robot = Robot()
        
        # Initialize the devices
        self.left_wheel_motor = self.robot.getDevice('left wheel motor')
        self.right_wheel_motor = self.robot.getDevice('right wheel motor')
        self.ps_sensors = [self.robot.getDevice(f'ps{i}') for i in range(8)]
        self.ls_sensors = [self.robot.getDevice(f'ls{i}') for i in range(8)]

        # Check if all devices are properly initialized
        if not self.left_wheel_motor or not self.right_wheel_motor:
            print("Error: One or both motors were not found.")
        if any(sensor is None for sensor in self.ps_sensors + self.ls_sensors):
            print("Error: One or more sensors were not found.")

        # Enable sensors
        for sensor in self.ps_sensors + self.ls_sensors:
            if sensor:
                sensor.enable(TIME_STEP)

        # Set initial motor velocities
        self.left_wheel_motor.setVelocity(0.0)
        self.right_wheel_motor.setVelocity(0.0)

    def get_sensor_data(self):
        # Get sensor values
        ps_data = [sensor.getValue() for sensor in self.ps_sensors]
        ls_data = [sensor.getValue() for sensor in self.ls_sensors]
        return ps_data, ls_data

    def set_motor_velocity(self, left_velocity, right_velocity):
        # Set motor velocities
        self.left_wheel_motor.setVelocity(left_velocity)
        self.right_wheel_motor.setVelocity(right_velocity)

    def run(self):
        # Main loop
        while self.robot.step(TIME_STEP) != -1:
            ps_data, ls_data = self.get_sensor_data()
            print("Proximity Sensor Data:", ps_data)
            print("Light Sensor Data:", ls_data)
            # Example behavior
            if all(value > 50 for value in ps_data):
                self.set_motor_velocity(1.0, 1.0)
            else:
                self.set_motor_velocity(0.0, 0.0)

if __name__ == "__main__":
    controller = EPUCKController()
    controller.run()
