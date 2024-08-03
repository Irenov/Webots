from controller import Supervisor
import math
import random

TIME_STEP = 64
BROKEN_SENSOR = "right sensor"

class SupervisorController(Supervisor):
    def __init__(self):
        super().__init__()

        # Retrieve robot nodes by DEF name
        self.robots = [self.getFromDef(f'ROBOT_{i + 1}') for i in range(6)]
        self.print_robot_types()

        self.hexagon_positions = self.get_hexagon_positions(1.0)
        self.initialize_robots()

    def print_robot_types(self):
        for i, robot in enumerate(self.robots):
            if robot is None:
                print(f"Error: Robot ROBOT_{i + 1} not found. Check DEF name in the world file.")
            else:
                node_type = robot.getType()
                print(f"Node ROBOT_{i + 1} type ID: {node_type}")

                if node_type == 34:  # 34 corresponds to Robot type
                    print(f"Robot ROBOT_{i + 1} initialized successfully.")
                else:
                    print(f"Error: Node ROBOT_{i + 1} is not a Robot object. Expected type ID 34 but found '{node_type}'.")

    def get_hexagon_positions(self, radius):
        positions = []
        angle = 2 * math.pi / 6
        for i in range(6):
            x = radius * math.cos(i * angle)
            y = radius * math.sin(i * angle)
            positions.append((x, y, 0))
        return positions

    def initialize_robots(self):
        for i, robot in enumerate(self.robots):
            if robot:
                x, y, z = self.hexagon_positions[i]
                translation_field = robot.getField('translation')
                if translation_field:
                    translation_field.setSFVec3f([x, y, z])
                    print(f"Initialized robot ROBOT_{i + 1} at position {x}, {y}, {z}")
                else:
                    print(f"Error: Translation field not found for robot ROBOT_{i + 1}")

    def get_sensor_data(self):
        ps_data = []
        ls_data = []
        for i, robot in enumerate(self.robots):
            if robot:
                node_type = robot.getType()
                print(f"Fetching sensor data from robot {i + 1}. Node type ID: {node_type}")

                if node_type == 34:  # Verify this ID corresponds to Robot
                    ps_data.append([self.get_sensor_value(robot, f'ps{j}') for j in range(8)])
                    ls_data.append([self.get_sensor_value(robot, f'ls{j}') for j in range(8)])
                else:
                    print(f"Error: Node ROBOT_{i + 1} is not a Robot object. Skipping robot.")
                    ps_data.append([0] * 8)
                    ls_data.append([0] * 8)
            else:
                print(f"Skipping data retrieval for robot ROBOT_{i + 1} due to invalid reference.")
                ps_data.append([0] * 8)
                ls_data.append([0] * 8)
        return ps_data, ls_data

    def get_sensor_value(self, robot, sensor_name):
        try:
            if robot.getType() == 34:  # Check if it's a valid Robot node
                sensor = robot.getDevice(sensor_name)
                if sensor:
                    sensor.enable(TIME_STEP)
                    return sensor.getValue()
                else:
                    print(f"Error: Sensor {sensor_name} not found in robot.")
                    return 0
            else:
                print(f"Error: Node is not a Robot object, cannot get sensor {sensor_name}.")
                return 0
        except Exception as e:
            # print(f"Exception occurred while retrieving sensor {sensor_name}: {e}")
            return 0

    def reconfigure_robots(self):
        ps_data, ls_data = self.get_sensor_data()
        for i, robot in enumerate(self.robots):
            if robot:
                if min(ps_data[i]) < 50:
                    x, y, z = self.hexagon_positions[i]
                    translation_field = robot.getField('translation')
                    if translation_field:
                        new_x = x + 0.1  # Example adjustment
                        translation_field.setSFVec3f([new_x, y, z])
                        print(f"Reconfigured robot ROBOT_{i + 1} to new position {new_x}, {y}, {z}")
            else:
                print(f"Skipping reconfiguration for robot ROBOT_{i + 1} due to invalid reference")

    def run(self):
        while self.step(TIME_STEP) != -1:
            self.reconfigure_robots()

if __name__ == "__main__":
    supervisor = SupervisorController()
    supervisor.run()
