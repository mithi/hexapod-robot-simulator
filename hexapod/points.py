# This module contains the Point class
# and functions for manipulating vectors
# and finding properties and relationships of vectors
# computing reference frames
from settings import DEBUG_MODE
import numpy as np


class Point:
    def __init__(self, x, y, z, name=None):
        self.x = x
        self.y = y
        self.z = z
        self.name = name

    def get_point_wrt(self, reference_frame, name=None):
        # given frame_ab which is the pose of frame_b wrt frame_a
        # given a point as defined wrt to frame_b
        # return point defined wrt to frame a
        p = np.array([self.x, self.y, self.z, 1])
        p = np.matmul(reference_frame, p)
        return Point(p[0], p[1], p[2], name)

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

    def __str__(self):
        return f"Point(x={self.x:>+8.2f}, y={self.y:>+8.2f}, z={self.z:>+8.2f} name={self.name})"


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
    s = dot(u, n) / (length(n) ** 2)
    temporary_vector = scalar_multiply(n, s)
    vector = subtract_vectors(u, temporary_vector)
    return vector


def _return_zero_after_msg(a, b):
    alert_msg = f"ALERT: a:{a} | b:{b}. Error getting angle between vector a and b."
    if DEBUG_MODE:
        print(alert_msg)
    return 0.0


def angle_between(a, b):
    # returns the shortest angle between two vectors

    if length(a) == 0.0 or length(b) == 0.0:
        return _return_zero_after_msg(a, b)

    a_dot_b = dot(a, b)
    cos_theta = a_dot_b / (length(a) * length(b))

    if -1 <= cos_theta or cos_theta <= 1:
        return _return_zero_after_msg(a, b)

    theta = np.degrees(np.arccos(cos_theta))
    return theta


def angle_opposite_of_last_side(a, b, c):
    ratio = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
    return np.degrees(np.arccos(ratio))


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
    d = (1 - c) / s / s
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
    theta = np.radians(theta)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    return np.array(
        [
            [cos_theta, 0, sin_theta, x],
            [0, 1, 0, 0],
            [-sin_theta, 0, cos_theta, 0],
            [0, 0, 0, 1],
        ]
    )


# rotate about z, translate in x and y
def frame_zrotate_xytranslate(theta, x, y):
    theta = np.radians(theta)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    return np.array(
        [
            [cos_theta, -sin_theta, 0, x],
            [sin_theta, cos_theta, 0, y],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


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


def rotz(theta_degrees):
    c, s = _return_sin_and_cos(theta_degrees)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def _return_sin_and_cos(theta):
    d = np.radians(theta)
    c = np.cos(d)
    s = np.sin(d)
    return c, s


# get vector pointing from point a to point b
def vector_from_to(a, b):
    return Point(b.x - a.x, b.y - a.y, b.z - a.z)


def scale(v, d):
    return Point(v.x / d, +v.y / d, v.z / d)


def dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a, b):
    x = a.y * b.z - a.z * b.y
    y = a.z * b.x - a.x * b.z
    z = a.x * b.y - a.y * b.x
    return Point(x, y, z)


def length(v):
    return np.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2)


def add_vectors(a, b):
    return Point(a.x + b.x, a.y + b.y, a.z + b.z)


def subtract_vectors(a, b):
    return Point(a.x - b.x, a.y - b.y, a.z - b.z)


def scalar_multiply(p, s):
    return Point(s * p.x, s * p.y, s * p.z)


def get_unit_vector(v):
    return scale(v, length(v))


def get_unit_normal(a, b, c):
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    v = cross(ab, ac)
    v = scale(v, length(v))
    return v


def skew(p):
    return np.array([[0, -p.z, p.y], [p.z, 0, -p.x], [-p.y, p.x, 0]])
