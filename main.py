from population import Population
from plane import Vector
from lander import State

MUTATION_RATE = 0.08
MAX_LIFECYCLE = 100
POPULATION_SIZE = 100
REFRESH_RATE = 30
MAP_SELECTION = 1


def ground_inputs_to_line(ground_points):
    points = []
    for point in ground_points:
        points.append(Vector(*map(int, point.split())))
    return points


def init():
    input1 = [6,  # number of ground points
              "0 1500", "1000 2000", "2000 500", "3500 500", "5000 1500", "6999 1000",
              "5000 2500",  # INIT_X INIT_Y
              "0 0",  # INIT_DX INIT_DY
              "0"]  # INIT_ANGLE
    input2 = [15,  # number of ground points
              "0 2500", "100 200", "500 150", "1000 2000", "2000 2000", "2010 1500", "2200 800", "2500 200",
              "6899 300", "6999 2500", "4100 2600", "4200 1000", "3500 800", "3100 1100", "3400 2900",
              "6500 1300",  # INIT_X INIT_Y #16
              "-50 0",  # INIT_DX INIT_DY #17
              "0"]  # INIT_ANGLE #18

    input3 = [15,  # number of ground points
              "0 2500", "100 200", "500 150", "1000 2000", "2000 2000", "2010 1500", "2200 800", "2500 200",
              "6899 300", "6999 2500", "4100 2600", "4200 1000", "3500 800", "3100 1100", "3400 2900",
              "6500 1300",  # INIT_X INIT_Y #16
              "0 0",  # INIT_DX INIT_DY #17
              "0"]  # INIT_ANGLE #18

    input_data_list = list([input1, input2, input3])
    input_data = input_data_list[MAP_SELECTION]
    num_ground_points = input_data[0]
    ground_points = input_data[1: 1+num_ground_points]
    init_pos = input_data[1+num_ground_points]
    init_speed = input_data[2+num_ground_points]
    init_angle = input_data[3+num_ground_points]

    # parse into point object
    ground_points = ground_inputs_to_line(ground_points)
    init_pos = Vector(*map(int, init_pos.split()))
    init_speed = Vector(*map(int, init_speed.split()))
    init_angle = int(init_angle)

    init_state = State(fuel=1000,
                       power=0,
                       angle=init_angle,
                       speed=Vector(init_speed.x, init_speed.y),
                       position=Vector(init_pos.x, init_pos.y),
                       acceleration=Vector(0, 0))

    population = Population(mutation_rate=MUTATION_RATE,
                            pop_size=POPULATION_SIZE,
                            ground_points=ground_points,
                            init_state=init_state,
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
