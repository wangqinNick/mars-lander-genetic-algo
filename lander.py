import math
from turtle import Turtle
from plane import Vector
from enum import Enum

GRAVITY = Vector(0.0, -2.00)
MAX_X = 6999
MIN_X = 0


def get_distance(x0, y0, x1, y1):
    # Todo: calculate and return the surface distance from the collision point and safe zone
    distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    return distance


def get_distance_landing(ground_list,
                         landing_zone_index,  # 4
                         landing_index,  # 2
                         x1,
                         y1
                         ):
    if landing_index > landing_zone_index:
        surface_distance = 0.0
        for i in range(landing_zone_index, landing_index):
            x0_ = ground_list[i].x
            y0_ = ground_list[i].y
            x1_ = ground_list[i + 1].x
            y1_ = ground_list[i + 1].y

            segment_distance = get_distance(x0=x0_,
                                            y0=y0_,
                                            x1=x1_,
                                            y1=y1_)
            surface_distance += segment_distance
        x0 = ground_list[landing_index].x
        y0 = ground_list[landing_index].y
        segment_distance = get_distance(x0, y0, x1, y1)
        surface_distance += segment_distance
        return surface_distance
    else:
        # left-hand side
        surface_distance = 0.0
        for i in range(landing_index + 1,  # 3
                       landing_zone_index  # 4
                       ):
            x0_ = ground_list[i].x
            y0_ = ground_list[i].y
            x1_ = ground_list[i + 1].x
            y1_ = ground_list[i + 1].y

            segment_distance = get_distance(x0=x0_,
                                            y0=y0_,
                                            x1=x1_,
                                            y1=y1_)
            surface_distance += segment_distance
        x0 = ground_list[landing_index + 1].x
        y0 = ground_list[landing_index + 1].y
        segment_distance = get_distance(x0, y0, x1, y1)
        surface_distance += segment_distance
        return surface_distance


def coerce_range(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


class State:
    def __init__(self, fuel, power, angle, speed, position, acceleration):
        self.fuel = fuel
        self.power = power
        self.angle = angle
        self.position = position
        self.speed = speed
        self.acceleration = acceleration


class ControlCommands:
    def __init__(self, angle, power):
        """
        :param angle: 0, 1, 2, 3, 4
        :param power:  -90, -75, ... , 0, +15, +30, ..., +75, +90
        """
        self.angle = angle
        self.power = power


class FlyState(Enum):
    """
    Represented lander flying state
    """
    Landed = 1
    Crashed = 2
    Flying = 3
    Landed_In_Zone = 4


class Lander:
    GROUND = None
    LANDING_ZONE_MARK = None

    def __init__(self, init_state, chromosome, ground):
        self.trajectory = [init_state]
        self.flystate = FlyState.Flying
        self.chromosome = chromosome
        Lander.GROUND = ground
        self.landing_zone = []
        self.fitness = 0.0
        self.hit_mark = -1  # mark the hitting point of the Lander
        self.status = FlyState.Flying
        self.distance = None

        self.compute_trajectory()
        self.calculate_fitness()

    def compute_trajectory(self):
        """
        compute the whole trajectory for the Lander and connect to the trajectory list
        """
        # Run the whole life of the chromosome in one cycle
        for i, cmd in enumerate(self.chromosome):
            current_state = self.trajectory[i]
            cmd = self.chromosome[i]
            next_state = self.compute_next_state(current_state, cmd)
            self.trajectory.append(next_state)
            if self.evaluate_outside(next_state):
                break
            if self.evaluate_hit_ground(current_state, next_state):
                break
            if self.evaluate_no_fuel(next_state):
                break
        self.calculate_distance()
        return

    @classmethod
    def compute_next_state(cls, current_state, cmd):
        next_state_angle = current_state.angle + cmd.angle
        next_state_power = coerce_range(current_state.power + cmd.power, 0, 4)
        thrust = Vector(0.0, 1.0).scale(next_state_power).rotate(next_state_angle)
        next_state_acceleration = current_state.acceleration.add(thrust).add(GRAVITY)
        next_state_speed = current_state.speed.add(current_state.acceleration).round_up()
        next_state_position = current_state.position.add(current_state.speed).round_up()
        next_state_fuel = current_state.fuel - next_state_power

        return State(fuel=next_state_fuel,
                     power=next_state_power,
                     angle=next_state_angle,
                     speed=next_state_speed,
                     position=next_state_position,
                     acceleration=next_state_acceleration)

    def evaluate_hit_ground(self, current_state, next_state):
        Lander.find_landing_zone()

        # Calculate the landing status (next state)
        # 0, for landing in landing zone
        # 1, for crashing on the ground
        # 2, for flying
        landing_status, self.hit_mark = Vector.is_line_crossing_other(current_state.position,
                                                                      next_state.position,
                                                                      Lander.GROUND,
                                                                      Lander.LANDING_ZONE_MARK)
        # print(self.land_index)
        if landing_status == 0 or landing_status == 1:  # landing or crashing
            if (next_state.angle == 0  # landing angle
                    and abs(next_state.speed.x) <= 40  # landing vertical speed
                    and abs(next_state.speed.y) <= 20  # landing horizontal speed
                    and landing_status == 0):  # landing in landing zone
                self.status = FlyState.Landed
            else:
                self.status = FlyState.Crashed
            return True
        return False

    def evaluate_hit_target(self, next_state, target):
        if (target.x - 10 < next_state.position.x <= target.x + 10 and
                target.y - 10 < next_state.position.y <= target.y + 10):
            self.status = FlyState.Landed
            return True

    def evaluate_no_fuel(self, next_state):
        """
        Evaluate if next state will be out of fuel
        :param next_state: next lander
        :return: True, if next state will be out of fuel; False, otherwise
        """
        if next_state.fuel <= 0:
            self.status = FlyState.Crashed
            return True
        return False

    def evaluate_outside(self, next_state):
        """
        Evaluate if next state will be outside the frame
        :param next_state: next lander
        :return: True, if next state will be outside the frame; False, otherwise
        """
        if next_state.position.x > MAX_X or next_state.position.x < MIN_X:
            self.flystate = FlyState.Crashed
            return True
        return False

    @classmethod
    def find_landing_zone(cls):
        """
        Find the [Left point] of the landing zone (the id)
        """
        for i in range(1, len(cls.GROUND)):
            if cls.GROUND[i - 1].y == cls.GROUND[i].y:
                cls.LANDING_ZONE_MARK = i - 1
                return

    def calculate_distance(self):
        if self.status == FlyState.Flying:
            self.calculate_distance_flying()
        else:
            self.calculate_distance_landing()

    def calculate_distance_landing(self):
        if self.hit_mark != -1:
            distance = get_distance_landing(ground_list=Lander.GROUND,
                                            landing_zone_index=Lander.LANDING_ZONE_MARK,
                                            landing_index=self.hit_mark,
                                            x1=self.trajectory[-1].position.x,
                                            y1=self.trajectory[-1].position.y)
            self.distance = distance

    def calculate_distance_flying(self):
        distance = get_distance(Lander.GROUND[Lander.LANDING_ZONE_MARK].x,
                                Lander.GROUND[Lander.LANDING_ZONE_MARK].y,
                                self.trajectory[-1].position.x,
                                self.trajectory[-1].position.y)
        self.distance = distance

    def calculate_fitness(self):
        distance = self.distance
        if distance < 1:
            distance = 1
        self.fitness = (1 / distance) ** 5
        if self.status == FlyState.Crashed:
            self.fitness *= 0.1
        if self.status == FlyState.Landed:
            self.fitness **= 4
