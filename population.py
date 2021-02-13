import numpy as np
from lander import Lander, State
from chromosome import Chromosome
from plane import Vector
from matplotlib import pyplot as plt
from collections import namedtuple
from copy import deepcopy

CMD_TUPLE = namedtuple("Command", ["angle", "power"])


def ground_inputs_to_line(ground_points):
    points = []
    for point in ground_points:
        points.append(Vector(*map(int, point.split())))
    return points


class Population:
    """
    A class to describe a population, where each member
    is an instance of a chromosome class
    """
    CHROMOSOME_SIZE = 50
    MAX_LIFETIME = 20
    X = 5000
    Y = 2500
    ANGLE = 0
    DX = 0
    DY = 0
    FUEL = 2000
    total_distance = None

    INIT_STATE = State(fuel=FUEL,
                       power=0,
                       angle=ANGLE,
                       speed=Vector(0, 0),
                       position=Vector(X, Y),
                       acceleration=Vector(0, 0))

    def __init__(self, mutation_rate, pop_size, ground_points):
        self.mutation_rate = mutation_rate
        self.population = []
        self.mating_pool = []
        self.population_size = pop_size
        self.generation_count = 1
        self.batch_simulations = []
        self.all_simulations = []

        self.ground_points = ground_inputs_to_line(ground_points)

        # create and run the landers
        for _ in range(self.population_size):
            new_lander = Lander(chromosome=Chromosome(Population.CHROMOSOME_SIZE),
                                init_state=Population.INIT_STATE,
                                ground=self.ground_points)
            self.population.append(new_lander)

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
        simulations = self.batch_simulations
        plt.ion()
        plt.title(f"Simulation of generation - {self.generation_count}")

        plt.clf()
        x, y = [], []
        for point in self.ground_points:
            x.append(point.x)
            y.append(point.y)
        plt.plot(x, y)

        for simulation in simulations:
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

        max_fitness = self.get_max_fitness()
        min_fitness = self.get_min_fitness()

        for i in range(self.population_size):
            if max_fitness == min_fitness:
                fitness_normalized = 1
            else:
                fitness_normalized = (self.population[i].fitness - min_fitness) / (max_fitness - min_fitness)
            times = int(fitness_normalized * 100)
            for j in range(times):
                self.mating_pool.append(self.population[i])

    def reproduction(self):
        self.population.clear()
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
                                          ground=self.ground_points))
            self.population.append(Lander(chromosome=child1,
                                          init_state=Population.INIT_STATE,
                                          ground=self.ground_points))
        # Increase the generation count
        self.generation_count += 1

    def calculate_pop_fitness(self):
        for i in self.population:
            i.calculate_fitness()

    def get_max_fitness(self):
        record = -1.0
        for i in self.population:
            if i.fitness > record:
                record = i.fitness
        return record

    def get_min_fitness(self):
        record = 10000000.0
        for i in self.population:
            if i.fitness < record:
                record = i.fitness
        return record
