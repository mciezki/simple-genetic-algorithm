import random
from math import sin, exp, pi


def generate_population(size, x_boundaries):
    lower_x_boundary, upper_x_boundary = x_boundaries
    population = []
    for i in range(size):
        individual = {
            'x': random.uniform(lower_x_boundary, upper_x_boundary)
        }
        population.append(individual)
    return population


def apply_function(individual):
    x = individual['x']
    return (exp(x)*sin(10*x*pi) + 1) / x + 5


def choice_by_roulette(sorted_population, fitness_sum):
    offset = 0
    normalized_fitness_sum = fitness_sum

    lowest_fitness = apply_function(sorted_population[0])
    if lowest_fitness < 0:
        offset = -lowest_fitness
        normalized_fitness_sum += offset * len(sorted_population)
    draw = random.uniform(0, 1)

    accumulated = 0
    for individual in sorted_population:
        fitness = apply_function(individual) + offset
        probability = fitness / normalized_fitness_sum
        accumulated += probability

        if draw <= accumulated:
            return individual


def sort_population_by_fitness(population):
    return sorted(population, key=apply_function)


def crossover(individual_a, individual_b):
    xa = individual_a['x']
    xb = individual_b['x']
    return {'x': (xa + xb) / 2}


def mutate(individual):
    next_x = individual['x'] + random.uniform(-interval, interval)
    lower_boundary, upper_boundary = x_boundaries

    # check boundaries:
    next_x = min(max(next_x, lower_boundary), upper_boundary)
    return {'x': next_x}


def reproduction(previous_population):
    next_generation = []
    sorted_by_fitness_population = sort_population_by_fitness(previous_population)
    population_size = len(previous_population)
    fitness_sum = sum(apply_function(individual) for individual in population)

    for i in range(population_size):
        probability = random.uniform(0, 1)
        first_choice = choice_by_roulette(sorted_by_fitness_population, fitness_sum)
        second_choice = choice_by_roulette(sorted_by_fitness_population, fitness_sum)

        if probability >= 0.5:
            individual = {'x': max(first_choice['x'], second_choice['x'])}
            next_generation.append(individual)

        elif probability <= 0.3:
            individual = crossover(first_choice, second_choice)
            next_generation.append(individual)

        else:
            individual = {'x': max(first_choice['x'], second_choice['x'])}
            individual = mutate(individual)
            next_generation.append(individual)
    return next_generation


#Parameters:
generations = 100
size = 50
x_boundaries = 0.5, 2.5
interval = 0.1


population = generate_population(size, x_boundaries)

for i in range(generations):
    print(f'\nGeneration {i+1}')

    for individual in population:
        print(individual, apply_function(individual))

    population = reproduction(population)

best_individual = sort_population_by_fitness(population)[-1]
print(f'\nBest position: {best_individual},\nResult: {round(apply_function(best_individual), 3)}')



