from collections import namedtuple
import random

CMD_TUPLE = namedtuple("Command", ["angle", "power"])


def coerce_range(value, min_value, max_value):
    """
    Converge the target value to a certain range [min_value, max_value]
    :param value: the target value
    :param min_value: lower bound
    :param max_value: upper bound
    :return: value after converging
    """
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


class Chromosome:
    MAX_THRUST_VALUE = 4
    MAX_THRUST_CHANGE = 2

    def __init__(self, size):
        self.genes = []
        self.gene_size = size
        self.genes.append(CMD_TUPLE(0, 0))  # Init values

        for i in range(1, self.gene_size):
            angle = coerce_range(
                self.genes[i - 1].angle + random.randint(-15, 16),
                -90, 90)
            power = coerce_range(
                self.genes[i - 1].power + random.randint(-1, 2),
                0, 4)
            self.genes.append(CMD_TUPLE(angle, power))

    def cross_over(self, partner):
        """
        Cross oneself with the partner chromosome
        :param partner: the partner chromosome
        :return: two children chromosomes
        """
        weight = random.random()
        weight_comp = 1 - weight
        child1 = Chromosome(len(self.genes))
        child2 = Chromosome(len(self.genes))

        for i in range(1, len(self.genes)):
            w_angle = int(self.genes[i].angle * weight + partner.genes[i].angle * weight_comp)
            w_power = int(self.genes[i].power * weight + partner.genes[i].power * weight_comp)
            child1.genes[i] = CMD_TUPLE(w_angle, w_power)

            w_angle = int(self.genes[i].angle * weight_comp + partner.genes[i].angle * weight)
            w_power = int(self.genes[i].power * weight_comp + partner.genes[i].power * weight)
            child2.genes[i] = CMD_TUPLE(w_angle, w_power)
        return child1, child2

    def mutate(self, mutation_rate):
        """
        Mutate the chromosome under the mutation rate
        :param mutation_rate: normally within [0 - 0.05]
        """
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                new_angle = coerce_range(
                    self.genes[i - 1].angle + random.randint(-15, 16),
                    -90, 90)
                new_power = coerce_range(
                    self.genes[i - 1].power + random.randint(-1, 2),
                    0, 4)
                self.genes[i] = (CMD_TUPLE(new_angle, new_power))
