# This module contains the Vector class
# and functions for manipulating vectors
# and finding properties and relationships of vectors
# computing reference frames
from math import sqrt, radians, sin, cos, degrees, acos, isnan
import numpy as np

from settings import DEBUG_MODE


class Vector:
    __slots__ = ("x", "y", "z", "name")

    def __init__(self, x, y, z, name=None):
        self.x = x
        self.y = y
        self.z = z
        self.name = name

    def get_point_wrt(self, reference_frame, name=None):
        """
        Given frame_ab which is the pose of frame_b wrt frame_a
        and that this point is defined wrt to frame_b
        Return point defined wrt to frame a
        """
        p = np.array([self.x, self.y, self.z, 1])
        p = np.matmul(reference_frame, p)
        return Vector(p[0], p[1], p[2], name)

    def update_point_wrt(self, reference_frame, z=0):
        p = np.array([self.x, self.y, self.z, 1])
        p = np.matmul(reference_frame, p)
        self.x = p[0]
        self.y = p[1]
        self.z = p[2] + z

    def move_xyz(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    def move_up(self, z):
        self.z += z

    @property
    def vec(self):
        return self.x, self.y, self.z

    def __repr__(self):
        s = f"Vector(x={self.x:>+8.2f}, y={self.y:>+8.2f}, z={self.z:>+8.2f}, name='{self.name}')"
        return s

    def __str__(self):
        return repr(self)

    def __eq__(self, other, percent_tol=0.0075):
        if not isinstance(other, Vector):
            return False

        tol = length(self) * percent_tol
        equal_val = np.allclose(self.vec, other.vec, atol=tol)
        equal_name = self.name == other.name
        return equal_val and equal_name


# *********************************************
# https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle
# https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/
# It works like this:
# - Walk clockwise or counterclockwise around the triangle
# and project the point onto the segment we are crossing
# by using the dot product.
# - Check that the vector created is on the same side
# for each of the triangle's segments
def is_point_inside_triangle(p, a, b, c):
    ab = (p.x - b.x) * (a.y - b.y) - (a.x - b.x) * (p.y - b.y)
    bc = (p.x - c.x) * (b.y - c.y) - (b.x - c.x) * (p.y - c.y)
    ca = (p.x - a.x) * (c.y - a.y) - (c.x - a.x) * (p.y - a.y)
    # must be all positive or all negative
    return (ab < 0.0) == (bc < 0.0) == (ca < 0.0)


def is_triangle(a, b, c):
    return (a + b > c) and (a + c > b) and (b + c > a)


# https://www.maplesoft.com/support/help/Maple/view.aspx?path=MathApps%2FProjectionOfVectorOntoPlane
# u is the vector, n is the plane normal
def project_vector_onto_plane(u, n):
    s = dot(u, n) / dot(n, n)
    temporary_vector = scalar_multiply(n, s)
    return subtract_vectors(u, temporary_vector)


def might_print_angle_between_error(a, b):
    if DEBUG_MODE:
        print(
            f"❗❗❗ERROR: angle_between({a}, {b}) is NAN\
        ... One of the might be a zero vector\
        ... the vectors might be pointing at the same direction or\
        ... something else entirely. 🤔"
        )


def angle_between(a, b):
    # returns the shortest angle between two vectors
    cos_theta = dot(a, b) / sqrt(dot(a, a) * dot(b, b))
    theta = degrees(acos(cos_theta))

    if isnan(theta):
        might_print_angle_between_error(a, b)
        return 0.0

    return theta


def angle_opposite_of_last_side(a, b, c):
    ratio = (a * a + b * b - c * c) / (2 * a * b)
    return degrees(acos(ratio))


# Check if angle from vector a to b about normal n is positive
# Rotating from vector a to is moving into a conter clockwise direction
def is_counter_clockwise(a, b, n):
    return dot(a, cross(b, n)) > 0


# https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
def frame_to_align_vector_a_to_b(a, b):
    v = cross(a, b)
    s = length(v)

    # When angle between a and b is zero or 180 degrees
    # cross product is 0, R = I
    if s == 0.0:
        return np.eye(4)
    c = dot(a, b)
    i = np.eye(3)  # Identity matrix 3x3

    # skew symmetric cross product
    vx = skew(v)
    d = (1 - c) / (s * s)
    r = i + vx + np.matmul(vx, vx) * d

    # r00 r01 r02 0
    # r10 r11 r12 0
    # r20 r21 r22 0
    #  0   0   0  1
    r = np.hstack((r, [[0], [0], [0]]))
    r = np.vstack((r, [0, 0, 0, 1]))
    return r


# rotate about y, translate in x
def frame_yrotate_xtranslate(theta, x):
    c, s = _return_sin_and_cos(theta)

    return np.array([[c, 0, s, x], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])


# rotate about z, translate in x and y
def frame_zrotate_xytranslate(theta, x, y):
    c, s = _return_sin_and_cos(theta)

    return np.array([[c, -s, 0, x], [s, c, 0, y], [0, 0, 1, 0], [0, 0, 0, 1]])


def frame_rotxyz(a, b, c):
    rx = rotx(a)
    ry = roty(b)
    rz = rotz(c)
    rxy = np.matmul(rx, ry)
    rxyz = np.matmul(rxy, rz)
    return rxyz


def rotx(theta):
    c, s = _return_sin_and_cos(theta)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])


def roty(theta):
    c, s = _return_sin_and_cos(theta)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])


def rotz(theta):
    c, s = _return_sin_and_cos(theta)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def _return_sin_and_cos(theta):
    d = radians(theta)
    c = cos(d)
    s = sin(d)
    return c, s


# get vector pointing from point a to point b
def vector_from_to(a, b):
    return Vector(b.x - a.x, b.y - a.y, b.z - a.z)


def scale(v, d):
    return Vector(v.x / d, v.y / d, v.z / d)


def dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a, b):
    x = a.y * b.z - a.z * b.y
    y = a.z * b.x - a.x * b.z
    z = a.x * b.y - a.y * b.x
    return Vector(x, y, z)


def length(v):
    return sqrt(dot(v, v))


def add_vectors(a, b):
    return Vector(a.x + b.x, a.y + b.y, a.z + b.z)


def subtract_vectors(a, b):
    return Vector(a.x - b.x, a.y - b.y, a.z - b.z)


def scalar_multiply(p, s):
    return Vector(s * p.x, s * p.y, s * p.z)


def get_unit_vector(v):
    return scale(v, length(v))


def get_normal_given_three_points(a, b, c):
    """
    Get the unit normal vector to the
    plane defined by the points a, b, c.
    """
    ab = vector_from_to(a, b)
    ac = vector_from_to(a, c)
    v = cross(ab, ac)
    v = scale(v, length(v))
    return v


def skew(p):
    return np.array([[0, -p.z, p.y], [p.z, 0, -p.x], [-p.y, p.x, 0]])
