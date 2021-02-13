from math import cos, sin, radians, sqrt


class Point:
    """
    Fundamental element
    Used to represent location
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, speed, time=1):
        return Point(self.x + speed.h_speed * time, self.y + speed.v_speed * time)

    def round_up(self):
        return Point(round(self.x), round(self.y))

    def get_vector(self):
        return Vector(self.x, self.y)


class Vector:
    """
    Basic element
    Used to represent speed, acceleration of the spaceship
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        """
        Add with another vector object
        :param other: another vector object
        :return The vector sum
        """
        x_ = self.x + other.x
        y_ = self.y + other.y
        return Vector(x_, y_)

    def rotate(self, angle):
        """
        Rotate a vector by a specific angle (in degree)
        :param angle: a specific angle (in degree)
        :return: The rotated vector
        """
        theta = radians(angle)
        cos_ = cos(theta)
        sin_ = sin(theta)
        return Vector(self.x * cos_ - self.y * sin_, self.x * sin_ + self.y * cos_)

    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def scale(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def round_up(self):
        return Vector(round(self.x), round(self.y))

    @classmethod
    def is_line_crossing_other(cls, a, b, lines, landing_zone_index):
        """
        Check if a segment (represented by ab) crosses with a list of lines
        :param landing_zone_index: index (left) of the landing zone
        :param a: vector a on segment
        :param b: vector b on segment
        :param lines: a list of lines
        :return: 0, if intersected with landing ground line
                 1, if intersected with normal ground lines
                 2, if not intersected with ground lines
        """
        for i in range(len(lines)):
            if cls.do_intersect(a, b, lines[i - 1], lines[i]):
                if i - 1 == landing_zone_index:
                    return 0, i - 1
                else:
                    return 1, i - 1
        else:
            return 2, -1

    @classmethod
    def get_orientation(cls, p, q, r):
        """
        Calculate the geometry status of three vectors
        :param p: vector p
        :param q: vector q
        :param r: vector =r
        :return: 0, if the three vectors are collinear;
                 1, if clockwise
                 2, if counter-clockwise
        """
        val = int(q.y - p.y) * int(r.x - q.x) - int(q.x - p.x) * int(r.y - q.y)
        if val == 0:
            # Collinear
            return 0
        if val > 0:
            return 1
        return 2

    @classmethod
    def on_segment(cls, p, q, r):
        """
        Check if vector p is on a segment represented by vector p and r
        :param p: segment vector p
        :param q: vector q to check
        :param r: segment vector r
        :return: True, if vector p is on a segment represented by vector p and r;
                 False, otherwise
        """
        return max(p.x, r.x) >= q.x >= min(p.x, r.x) and max(p.y, r.y) >= q.y >= min(p.y, r.y)

    @classmethod
    def do_intersect(cls, p1, q1, p2, q2):
        """
        Check if two lines (segments) intersect
        :param p1: vector on segment 1
        :param q1: vector on segment 1
        :param p2: vector on segment 2
        :param q2: vector on segment 2
        :return: True, if two lines intersect; False, otherwise
        """
        o1 = cls.get_orientation(p1, q1, p2)
        o2 = cls.get_orientation(p1, q1, q2)
        o3 = cls.get_orientation(p2, q2, p1)
        o4 = cls.get_orientation(p2, q2, q1)

        # General Case
        if o1 != o2 and o3 != o4:
            return True

        # Special Cases
        # p1, q1 and p2 are collinear and p2 lies on segment p1q1
        if o1 == 0 and cls.on_segment(p1, p2, q1):
            return True

        # p1, q1 and q2 are collinear and q2 lies on segment p1q1
        if o2 == 0 and cls.on_segment(p1, q2, q1):
            return True

        # p2, q2 and p1 are collinear and p1 lies on segment p2q2
        if o3 == 0 and cls.on_segment(p2, p1, q2):
            return True

        # p2, q2 and q1 are collinear and q1 lies on segment p2q2
        if o4 == 0 and cls.on_segment(p2, q1, q2):
            return True

        return False
