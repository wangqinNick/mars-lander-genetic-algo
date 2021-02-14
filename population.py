from collections import namedtuple
from copy import deepcopy

import numpy as np
from matplotlib import pyplot as plt

from chromosome import Chromosome
from lander import Lander

CMD_TUPLE = namedtuple("Command", ["angle", "power"])


class Population:
    """
    A class to describe a population, where each member
    is an instance of a chromosome class
    """
    CHROMOSOME_SIZE = None
    MAX_LIFECYCLE = None
    total_distance = None

    INIT_STATE = None

    def __init__(self, mutation_rate, pop_size, init_state, ground_points, max_lifecycle):
        self.mutation_rate = mutation_rate
        self.population = []
        self.mating_pool = []
        self.population_size = pop_size
        self.generation_count = 1
        self.batch_simulations = []
        self.all_simulations = []
        Population.MAX_LIFECYCLE = max_lifecycle
        Population.CHROMOSOME_SIZE = max_lifecycle
        Population.INIT_STATE = init_state
        self.ground_points = ground_points

        # create and run the landers
        for _ in range(self.population_size):
            new_lander = Lander(chromosome=Chromosome(Population.CHROMOSOME_SIZE),
                                init_state=Population.INIT_STATE,
                                ground=self.ground_points,
                                max_lifecycle=Population.MAX_LIFECYCLE)
            self.population.append(new_lander)
        self.simulate()

    def simulate(self):
        """
        From each chromosome in population we create object
        of Lander class and compute trajectory
        """
        self.batch_simulations = []
        for member in self.population:
            self.batch_simulations.append(deepcopy(member.trajectory))
        self.all_simulations.append(deepcopy(self.batch_simulations))

    def display_current_population_simulation(self):
        """
        Plot trajectory of every chromosome of population
        for all generations
        """
        plt.ion()
        plt.title(f"Simulation of generation - {self.generation_count}")

        plt.clf()
        x, y = [], []
        for point in self.ground_points:
            x.append(point.x)
            y.append(point.y)
        plt.plot(x, y)

        for simulation in self.batch_simulations:
            x, y = [], []
            for state in simulation:
                x.append(state.position.x)
                y.append(state.position.y)
            plt.plot(x, y)

        plt.xlim([0, 7000])
        plt.ylim([0, 3000])
        plt.draw()
        plt.pause(0.01)

    def selection(self):
        self.mating_pool.clear()
        max_fitness, min_fitness, ave_fitness, ave_distance = self.evaluate_pop_fitness()
        # print(ave_fitness, ave_distance)
        for i in range(self.population_size):
            fitness_normalized = self.population[i].fitness / max_fitness
            times = int(fitness_normalized * 100)
            for j in range(times):
                self.mating_pool.append(self.population[i])

    def reproduction(self):
        # sort the population
        self.population.sort(key=lambda member: member.fitness, reverse=True)

        # elitism selection
        elitism_pool = []
        for i in range(int(0.2 * self.population_size)):
            elitism_pool.append(deepcopy(self.population[i]))

        self.population.clear()
        self.population.extend(deepcopy(elitism_pool))

        while len(self.population) < self.population_size:
            # Spin the wheel of fortune to pick two parents

            m = np.random.randint(len(self.mating_pool))
            d = np.random.randint(len(self.mating_pool))
            # Pick two parents
            mom = self.mating_pool[m]
            dad = self.mating_pool[d]
            # Get their genes
            mom_genes = mom.get_chromosome()
            dad_genes = dad.get_chromosome()
            # Mate their genes
            # Cross over rate = 1
            child0, child1 = mom_genes.cross_over(dad_genes)
            child0.mutate(self.mutation_rate)
            child1.mutate(self.mutation_rate)

            # Fill the new population with the new child
            self.population.append(Lander(chromosome=child0,
                                          init_state=Population.INIT_STATE,
                                          ground=self.ground_points,
                                          max_lifecycle=Population.MAX_LIFECYCLE))
            self.population.append(Lander(chromosome=child1,
                                          init_state=Population.INIT_STATE,
                                          ground=self.ground_points,
                                          max_lifecycle=Population.MAX_LIFECYCLE))
        # Increase the generation count
        self.simulate()
        self.generation_count += 1

    def evaluate_pop_fitness(self):
        max_fitness = self.population[0].fitness
        min_fitness = self.population[0].fitness
        sum_fitness = 0
        sum_distance = 0
        for i in self.population:
            if i.fitness > max_fitness:
                max_fitness = i.fitness
            if i.fitness < min_fitness:
                min_fitness = i.fitness
            sum_fitness += i.fitness
            sum_distance += i.distance
        ave_fitness = sum_fitness / self.population_size
        ave_distance = sum_distance / self.population_size
        return max_fitness, min_fitness, ave_fitness, ave_distance
