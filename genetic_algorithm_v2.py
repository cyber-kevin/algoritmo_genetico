###########################################
# Universidade Federal Rural de Pernambuco#
# Author: Kevin Vinícius Ferreira de Lima #
# Date: 2023-04-14                        #
# e-mail: devkevferreira@gmail.com        #
###########################################

# GENETIC ALGORITHM v2 : Added auto-adjusted mutation rate

from functions.matrix_functions import *

from random import randint, shuffle, random, seed
from math import factorial
from time import time
import matplotlib.pyplot as plt

seed(7)

class Individual:
    
    def __init__(self, chromosome: list):
        self.chromosome = chromosome
    
    def addDistance(self, distance: int):
        self.distance = distance
    
    def addFitness(self, fitness: int):
        self.fitness = fitness

    def __str__(self):      
        return str(self.chromosome) 


class GeneticAlgorithm:

    def __init__(self, number_of_individuals: int, mutation_percentage: float, number_of_generations: int, mutation_diversity_threshold: float = 0.8, mutation_diversity_factor: float = 0.9):
        self.number_of_individuals = number_of_individuals
        self.mutation_percentage = mutation_percentage
        self.number_of_generations = number_of_generations
        self.mutation_diversity_threshold = mutation_diversity_threshold
        self.mutation_diversity_factor = mutation_diversity_factor 
        self.global_max_distance = 0 
        self.global_max_fitness = 0  


    def generatePopulation(self, list_of_points):
        population = []
        saved_chromosomes = []
        max_length = factorial(len(list_of_points)) 

        for _ in range(self.number_of_individuals): 

            if len(population) == max_length: 
                break

            shuffle(list_of_points)
            individual = Individual(chromosome=list_of_points.copy())

            if individual.chromosome not in saved_chromosomes: 
                population.append(individual)
                saved_chromosomes.append(individual.chromosome.copy())

        self.population = population

    def fitness(self, coordinates):
        distance_population = []

        for individual in self.population:
            distance = calculateDistance(individual.chromosome, coordinates)
            distance_population.append(distance)
            individual.addDistance(distance)

            # Update the global maximum distance
            if distance > self.global_max_distance:
                self.global_max_distance = distance

        for individual in self.population:
            fitness = self.global_max_distance - individual.distance
            individual.addFitness(fitness)

            # Update the global maximum fitness
            if fitness > self.global_max_fitness:
                self.global_max_fitness = fitness
        
    def survivor_selection(self):
        winners = []

        for _ in range(len(self.population)): 
            individual_one = self.population[randint(0, len(self.population)-1)]
            individual_two = self.population[randint(0, len(self.population)-1)]
        
            if individual_one.fitness > individual_two.fitness:
                winners.append(individual_one)
            else:
                winners.append(individual_two)
        
        self.population = winners
        
    def crossover(self, length):
        offsprings = []

        current_i = 0
        next_i = 1

        for i in range(int(len(self.population)/2)):
            parent_one = self.population[i+current_i].chromosome
            parent_two = self.population[i+next_i].chromosome
            parents = [parent_two, parent_one] 

            cut = randint(0, length-1)

            piece_parent_one = parent_one[:cut] 
            piece_parent_two = parent_two[:cut]
            pieces = [piece_parent_one, piece_parent_two]

            for i in range(len(pieces)): 
                offspring = pieces[i]

                for gene in parents[i]:
                    if gene not in offspring:
                        offspring.append(gene)

                offspring = Individual(chromosome=offspring)
                
                offsprings.append(offspring)
            
            current_i += 1
            next_i += 1

        self.population = offsprings

    def mutation(self):
        unique_chromosomes = set(tuple(individual.chromosome) for individual in self.population)
        diversity = len(unique_chromosomes) / len(self.population)

        if diversity < self.mutation_diversity_threshold:
            self.mutation_percentage /= self.mutation_diversity_factor

        else:
            self.mutation_percentage *= self.mutation_diversity_factor

        for individual in self.population:
            m = random()

            if m <= self.mutation_percentage:
                pos1 = randint(0, len(individual.chromosome)-1)
                pos2 = randint(0, len(individual.chromosome)-1)

                individual.chromosome[pos1], individual.chromosome[pos2] = individual.chromosome[pos2], individual.chromosome[pos1]
        

if __name__ == '__main__':
    matrix = txtToMatrix('tests/matrix5.txt')
    coordinates = getCoordinates(matrix)
    list_of_points = getPoints(matrix)
    points_length = len(list_of_points)

    clock_start = time()

    min_distances = []
    ga = GeneticAlgorithm(number_of_individuals=300, mutation_percentage=0.05, number_of_generations=800)

    ga.generatePopulation(list_of_points=list_of_points)
    ga.fitness(coordinates=coordinates)

    for gen in range(ga.number_of_generations):
        min_distance = min(individual.distance for individual in ga.population)
        min_distances.append(min_distance)
        ga.survivor_selection()
        ga.crossover(length=points_length)
        ga.mutation()
        ga.fitness(coordinates=coordinates)

    max_fitness = -1
    fittest = None
    optimal_solution = None
    for individual in ga.population:
        if individual.fitness > max_fitness:
            max_fitness= individual.fitness
            fittest = individual
            optimal_solution = individual.chromosome 

    clock_end = time()

    print('#######################################')
    print()
    unique_chromosomes = set(tuple(i.chromosome) for i in ga.population)
    diversity = len(unique_chromosomes) / len(ga.population)
    print(f'UNIQUE CHROMOSOMES: {len(unique_chromosomes)} | ALL CHROMOSOMES: {len(ga.population)} | DIVERSITY: {diversity:.2f}')
    print(f'Mutation percentage: {ga.mutation_percentage:.2f}')
    print(f'Response time: {(clock_end - clock_start):.2f} seconds')
    print()
    print('#######################################')
    print()

    print(f'{" → ".join(optimal_solution)} | Distância: {fittest.distance} unidades')

    plt.plot(min_distances)
    plt.xlabel('Generation', fontsize=14)
    plt.ylabel('Minimum Distance', fontsize=14)
    plt.title('Convergence of Individuals', fontsize=18)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.show()


