from plane import Vector
from population import Population
from ground import Ground, SimpleTarget

MUTATION_RATE = 0.05
MAX_LIFECYCLE = 30


def init():
    ground_points = ["0 1500", "1000 2000", "2000 500", "3500 500",
                     "5000 1500", "6999 1000"]
    simple_target = SimpleTarget(5000, 2500)

    population = Population(mutation_rate=MUTATION_RATE,
                            pop_size=100,
                            ground_points=ground_points,
                            max_lifecycle=MAX_LIFECYCLE)
    return population


def evolve(population):
    population.selection()
    population.reproduction()


def main():
    generation_count = 0
    population = init()
    while True:
        evolve(population)
        print("Generation: {}".format(generation_count))
        if generation_count % 10 == 0:
            population.display_current_population_simulation()
        generation_count += 1

if __name__ == '__main__':
    main()
