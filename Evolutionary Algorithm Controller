from controller import Robot
import random
import math

TIME_STEP = 64
POPULATION_SIZE = 20
GENES = 10
MUTATION_RATE = 0.1
MAX_GENERATIONS = 100
MAX_VELOCITY = 6.28
COLLISION_PENALTY = 100
OBSTACLE_THRESHOLD = 800

class EPuckController(Robot):
    def __init__(self):
        super().__init__()
        self.left_motor = self.getDevice("left wheel motor")
        self.right_motor = self.getDevice("right wheel motor")
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)
        
        self.sensors = []
        for i in range(8):
            sensor = self.getDevice(f"ps{i}")
            sensor.enable(TIME_STEP)
            self.sensors.append(sensor)

        self.population = [self.create_chromosome() for _ in range(POPULATION_SIZE)]
    
    def create_chromosome(self):
        return [random.uniform(-1, 1) for _ in range(GENES)]
    
    def evaluate_fitness(self, chromosome):
        return self.run_robot(chromosome)
    
    def run_robot(self, chromosome):
        total_distance = 0
        collision_count = 0
        
        for _ in range(100):
            sensor_values = [sensor.getValue() for sensor in self.sensors]
            
            left_speed, right_speed = self.handle_obstacle(sensor_values)
            
            self.left_motor.setVelocity(left_speed)
            self.right_motor.setVelocity(right_speed)
            self.step(TIME_STEP)
            
            distance_traveled = (left_speed + right_speed) / 2 * TIME_STEP / 1000
            total_distance += distance_traveled
            
            if any(value > OBSTACLE_THRESHOLD for value in sensor_values):
                collision_count += 1
        
        fitness = total_distance - COLLISION_PENALTY * collision_count
        return fitness
    
    def handle_obstacle(self, sensor_values):
        # Check if any sensor detects an obstacle
        if any(value > OBSTACLE_THRESHOLD for value in sensor_values):
            # Implement a more aggressive avoidance strategy
            left_speed = -MAX_VELOCITY  # Move backward
            right_speed = MAX_VELOCITY  # Turn right
        else:
            # Move forward
            left_speed = MAX_VELOCITY
            right_speed = MAX_VELOCITY
        
        return left_speed, right_speed
    
    def evolve_population(self):
        fitnesses = [self.evaluate_fitness(chrom) for chrom in self.population]
        new_population = []
        for _ in range(POPULATION_SIZE//2):
            parent1, parent2 = self.select_parents(fitnesses)
            child1, child2 = self.crossover(parent1, parent2)
            new_population.extend([self.mutate(child1), self.mutate(child2)])
        self.population = new_population
    
    def select_parents(self, fitnesses):
        total_fitness = sum(fitnesses)
        
        if total_fitness == 0:
            # Handle the case where total fitness is zero
            raise ValueError("Total fitness is zero. Cannot select parents.")
        
        def pick_parent():
            pick = random.uniform(0, total_fitness)
            current = 0
            for i, fitness in enumerate(fitnesses):
                current += fitness
                if current > pick:
                    return self.population[i]
            return self.population[-1]  # Fallback to the last individual
    
        parent1 = pick_parent()
        parent2 = pick_parent()
        
        # Ensure we don't pick the same parent twice
        while parent2 == parent1:
            parent2 = pick_parent()
        
        return parent1, parent2


    
    def crossover(self, parent1, parent2):
        point = random.randint(1, GENES-1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    
    def mutate(self, chromosome):
        return [gene + random.uniform(-MUTATION_RATE, MUTATION_RATE) if random.random() < MUTATION_RATE else gene for gene in chromosome]

controller = EPuckController()

for generation in range(MAX_GENERATIONS):
    controller.evolve_population()
    print(f"Generation {generation} evolved.")

# After evolution, test the best individual (first in the population for simplicity)
best_chromosome = controller.population[0]
controller.run_robot(best_chromosome)
