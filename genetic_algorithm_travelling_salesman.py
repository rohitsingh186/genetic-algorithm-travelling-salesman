#
# Optimal (by program): cities 1-8-5-4-10-6-3-7-2-11-9-1 = 253km
#
import random
import time
import math

t1 = time.time()


def initialize():
    while len(population) < NUM_START_POPULATION:
        temp = list(CITIES)
        random.shuffle(temp)
        if not (temp in population):
            population.append(temp)
            
            
            
def evaluation_function(individual):
    num_cities = len(CITIES)
    path_cost = DISTANCE[(individual[num_cities - 1], individual[0])]
    i = 1
    while i < num_cities:
        path_cost += DISTANCE[(individual[i - 1], individual[i])]
        i += 1
    return (1000.0 / path_cost)


def best_fit():
    max_fitness_value = 0
    best_fit = []
    for temp in population:
        temp_fitness_value = evaluation_function(temp)
        if temp_fitness_value > max_fitness_value:
            max_fitness_value = temp_fitness_value
            best_fit = temp
    return best_fit, (1000.0 / max_fitness_value)
            
            
def selection():
    num = CROSSOVER_RATIO * len(population)
    if num % 2 != 0:
        num = num - 1
    fitness_values = []
    sum_fitness_value = 0
    for temp in population:
        temp_fitness_value = evaluation_function(temp)
        fitness_values.append(temp_fitness_value)
        sum_fitness_value += temp_fitness_value
    probability = []
    for temp in fitness_values:
        probability.append(float(temp) / sum_fitness_value)
    # Start selection process
    count = 0
    selected_individuals_idx = []
    while count < num:
        probability_left = sum(probability)
        lucky_number = random.random() * probability_left
        cumulative_sum = 0
        i = 0
        while cumulative_sum < lucky_number:

            cumulative_sum += probability[i]
            i += 1
        selected_individuals_idx.append(i - 1)
        probability[i - 1] = 0
        count += 1
    selected_individuals = [population[i] for i in selected_individuals_idx]
    print
    return selected_individuals
     
    
def heal(patient):
    size = len(patient)
    temp = range(1, size + 1)
    missing_cities = list(set(temp).difference(set(patient)))
    if len(missing_cities) != 0:
        i = 1
        while i < len(patient):
            if patient[i] in patient[0:i]:
                patient[i] = missing_cities[0]
                missing_cities.pop(0)
            i += 1
    return patient
    
    
def crossover(selected_individuals):
    selected_couples = [selected_individuals[i:i+2] for i in xrange(0, len(selected_individuals), 2)]
    new_generation = []
    for temp_couple in selected_couples:
        random_point = random.choice(range(1, len(CITIES)))
        temp1, temp2 =  temp_couple[0][0:random_point], temp_couple[0][random_point:len(CITIES)]
        temp3, temp4 =  temp_couple[1][0:random_point], temp_couple[1][random_point:len(CITIES)]
        temp1.extend(temp4)
        temp3.extend(temp2)
        temp1 = heal(temp1)
        temp3 = heal(temp3)
        new_generation.append(temp1)
        new_generation.append(temp3)
    return new_generation



def mutation(new_generation):
    num = math.ceil(len(new_generation) * MUTAION_RATIO)
    population_idx = range(len(new_generation))
    mutant_idx = []
    while len(mutant_idx) < num:
        selected_idx = random.choice(population_idx)
        mutant_idx.append(selected_idx)
        population_idx.remove(selected_idx)
    for temp_idx in mutant_idx:
        i = random.choice(range(len(CITIES)))
        j = random.choice(range(len(CITIES)))
        while i == j:
            i = random.choice(range(len(CITIES)))
            j = random.choice(range(len(CITIES)))
        temp = new_generation[temp_idx][i]
        new_generation[temp_idx][i] = new_generation[temp_idx][j]
        new_generation[temp_idx][j] = temp
    return new_generation
    
    

CITIES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
NUM_START_POPULATION = 8
DISTANCE = {(1, 1): 0, (1, 2): 29, (1, 3): 20, (1, 4): 21, (1, 5): 16, (1, 6): 31, (1, 7): 100, (1, 8): 12, (1, 9): 4, (1, 10): 31, (1, 11): 18,
            (2, 1): 29, (2, 2): 0, (2, 3): 15, (2, 4): 29, (2, 5): 28, (2, 6): 40, (2, 7): 72, (2, 8): 21, (2, 9): 29, (2, 10): 41, (2, 11): 12,
            (3, 1): 20, (3, 2): 15, (3, 3): 0, (3, 4): 15, (3, 5): 14, (3, 6): 25, (3, 7): 81, (3, 8): 9, (3, 9): 23, (3, 10): 27, (3, 11): 13,
            (4, 1): 21, (4, 2): 29, (4, 3): 15, (4, 4): 0, (4, 5): 4, (4, 6): 12, (4, 7): 92, (4, 8): 12, (4, 9): 25, (4, 10): 13, (4, 11): 25,
            (5, 1): 16, (5, 2): 28, (5, 3): 14, (5, 4): 4, (5, 5): 0, (5, 6): 16, (5, 7): 94, (5, 8): 9, (5, 9): 20, (5, 10): 16, (5, 11): 22,
            (6, 1): 31, (6, 2): 40, (6, 3): 25, (6, 4): 12, (6, 5): 16, (6, 6): 0, (6, 7): 95, (6, 8): 24, (6, 9): 36, (6, 10): 3, (6, 11): 37,
            (7, 1): 100, (7, 2): 72, (7, 3): 81, (7, 4): 92, (7, 5): 94, (7, 6): 95, (7, 7): 0, (7, 8): 90, (7, 9): 101, (7, 10): 99, (7, 11): 84,
            (8, 1): 12, (8, 2): 21, (8, 3): 9, (8, 4): 12, (8, 5): 9, (8, 6): 24, (8, 7): 90, (8, 8): 0, (8, 9): 15, (8, 10): 25, (8, 11): 13,
            (9, 1): 4, (9, 2): 29, (9, 3): 23, (9, 4): 25, (9, 5): 20, (9, 6): 36, (9, 7): 101, (9, 8): 15, (9, 9): 0, (9, 10): 35, (9, 11): 18,
            (10, 1): 31, (10, 2): 41, (10, 3): 27, (10, 4): 13, (10, 5): 16, (10, 6): 3, (10, 7): 99, (10, 8): 25, (10, 9): 35, (10, 10): 0, (10, 11): 38,
            (11, 1): 18, (11, 2): 12, (11, 3): 13, (11, 4): 25, (11, 5): 22, (11, 6): 37, (11, 7): 84, (11, 8): 13, (11, 9): 18, (11, 10): 38, (11, 11): 0}
CROSSOVER_RATIO = 0.5
MUTAION_RATIO = 0.2
POPULATION_LIMIT = 5000
population = []            


initialize()
print 'Initial Population:-'
for a in population:
    print a
print


while len(population) < POPULATION_LIMIT:
    print 'Current Population:-', len(population)
    selected_individuals = selection()
    new_generation = crossover(selected_individuals)
    new_generation = mutation(new_generation)
    population.extend(new_generation)
    
print
print 'Final Population:-', len(population)
for a in population:
    print a
print

optimal_path, path_cost = best_fit()
print 'Optimal Path:- ', optimal_path
print 'Path Cost:- ', path_cost

t2 = time.time()
print 'Time Taken: ', t2 - t1
