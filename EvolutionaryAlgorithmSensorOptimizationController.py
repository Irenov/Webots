from controller import Supervisor
import random
import math

TIME_STEP = 64
NUM_ROBOTS = 6
SENSOR_RANGE = 0.06
NUM_GENERATIONS = 50
NUM_CHILDREN = 10
INITIAL_POSITION_RADIUS = .4

supervisor = Supervisor()
robots = []

for i in range(NUM_ROBOTS):
    robot = supervisor.getFromDef(f'ROBOT_{i+1}')
    if robot:
        robots.append(robot)

def calculate_coverage(robots):
    coverage_map = set()  # Use a set to avoid double-counting coverage

    for robot in robots:
        position = robot.getPosition()
        rotation = robot.getField('rotation').getSFRotation()
        angle_offset = rotation[3]  # Rotation around Z-axis
        
        # For simplicity, consider a circular coverage area
        x, y = position[0], position[1]
        for angle in range(0, 360, 10):  # Sample points around the circle
            angle_rad = math.radians(angle + math.degrees(angle_offset))
            proj_x = x + SENSOR_RANGE * math.cos(angle_rad)
            proj_y = y + SENSOR_RANGE * math.sin(angle_rad)
            coverage_map.add((round(proj_x, 2), round(proj_y, 2)))

    coverage_area = len(coverage_map)
    return coverage_area

# Function to create children configurations
def create_children(parent_config):
    children = []

    for _ in range(NUM_CHILDREN):
        child = parent_config.copy()
        for robot_data in child:
            # Slightly modify the position and rotation of each robot
            robot_data['position'][0] += random.uniform(-INITIAL_POSITION_RADIUS, INITIAL_POSITION_RADIUS)
            robot_data['position'][1] += random.uniform(-INITIAL_POSITION_RADIUS, INITIAL_POSITION_RADIUS)
            robot_data['rotation'] += random.uniform(-math.pi, math.pi)
            if robot_data['position'][0] > INITIAL_POSITION_RADIUS or robot_data['position'][0] < -INITIAL_POSITION_RADIUS:
                robot_data['position'][0] = INITIAL_POSITION_RADIUS
            if robot_data['position'][1] > INITIAL_POSITION_RADIUS or robot_data['position'][1] < -INITIAL_POSITION_RADIUS:
                robot_data['position'][1] = INITIAL_POSITION_RADIUS
                
        children.append(child)
    return children

# Function for evolutionary algorithm
def evolutionary_algorithm(initial_config):
    best_config = initial_config
    best_coverage = calculate_coverage(robots)
    coverage_data = []  # Store coverage data for output

    for generation in range(NUM_GENERATIONS):
        children = create_children(best_config)
        for child in children:
            # Apply the child configuration to the robots
            for i, robot_data in enumerate(child):
                robots[i].getField('translation').setSFVec3f(robot_data['position'])
                robots[i].getField('rotation').setSFRotation([0, 0, 1, robot_data['rotation']])
            supervisor.step(TIME_STEP)  # Step the simulation to apply changes

            child_coverage = calculate_coverage(robots)
            
            if child_coverage > best_coverage:
                best_coverage = child_coverage
                best_config = child

        coverage_data.append(best_coverage)
        print(f"Generation {generation + 1}: Best coverage = {best_coverage} units")

    return best_config, best_coverage, coverage_data

def initialize_hexagon_config():
    config = []
    angle_increment = 2 * math.pi / NUM_ROBOTS

    for i in range(NUM_ROBOTS):
        angle = i * angle_increment
        x = INITIAL_POSITION_RADIUS * math.cos(angle)
        y = INITIAL_POSITION_RADIUS * math.sin(angle)
        config.append({
            'position': [x, y, 0.0],
            'rotation': random.uniform(0, 2 * math.pi)
        })
    
    return config

def initialize_random_config():
    config = []
    for _ in range(NUM_ROBOTS):
        config.append({
            'position': [random.uniform(-INITIAL_POSITION_RADIUS, INITIAL_POSITION_RADIUS),
                         random.uniform(-INITIAL_POSITION_RADIUS, INITIAL_POSITION_RADIUS),
                         0.0],
            'rotation': random.uniform(0, 2 * math.pi)
        })
    return config

# Main function
def main():
    initial_config = initialize_hexagon_config()
    
    best_config, best_coverage, coverage_data = evolutionary_algorithm(initial_config)
    print(f"Optimal configuration found with coverage area: {best_coverage} units")

    with open('coverage_data.txt', 'w') as f:
        for gen, coverage in enumerate(coverage_data, 1):
            f.write(f"Generation {gen}: {coverage} units\n")

    for i, robot_data in enumerate(initial_config):
        robots[i].getField('translation').setSFVec3f(robot_data['position'])
        robots[i].getField('rotation').setSFRotation([0, 0, 1, robot_data['rotation']])


if __name__ == "__main__":
    main()
