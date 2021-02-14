from population import Population

MUTATION_RATE = 0.05
MAX_LIFECYCLE = 100
REFRESH_RATE = 1


def init():
    ground_points_1 = ["0 1500", "1000 2000", "2000 500", "3500 500",
                       "5000 1500", "6999 1000"]
    ground_points_2 = ["0 2500", "100 200", "500 150",
                       "1000 2000", "2000 2000",
                       "2010 1500", "2200 800", "2500 200",
                       "6899 300", "6999 2500", "4100 2600",
                       "4200 1000", "3500 800", "3100 1100",
                       "3400 2900"]

    ground_points_list = list([ground_points_1,
                               ground_points_2])

    population = Population(mutation_rate=MUTATION_RATE,
                            pop_size=200,
                            ground_points=ground_points_list[2],
                            max_lifecycle=MAX_LIFECYCLE)
    population.display_current_population_simulation()
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
        if generation_count % REFRESH_RATE == 0:
            population.display_current_population_simulation()
        generation_count += 1


if __name__ == '__main__':
    main()
