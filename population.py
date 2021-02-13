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

    def __init__(self, gene_size, mutation_rate, pop_size, ground_points):
        self.mutation_rate = mutation_rate
        self.population = []
        self.mating_pool = []
        self.population_size = pop_size
        self.generation_count = 1
        self.batch_simulations = []
        self.all_simulations = []

        self.ground_points = ground_inputs_to_line(ground_points)

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
        lander_init_state = Population.INIT_STATE
        ground_line = ground_inputs_to_line(self.ground_points)
        for member in self.population:
            self.batch_simulations.append(deepcopy(member.trajectory))
