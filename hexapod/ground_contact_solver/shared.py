from math import isclose
from hexapod.points import (
    Vector,
    dot,
    cross,
    vector_from_to,
)

# Prioritize legs that are not adjacent to each other
SOME_LEG_TRIOS = [
    (0, 1, 3),
    (0, 1, 4),
    (0, 2, 3),
    (0, 2, 4),
    (0, 2, 5),
    (0, 3, 4),
    (0, 3, 5),
    (1, 2, 4),
    (1, 2, 5),
    (1, 3, 4),
    (1, 3, 5),
    (1, 4, 5),
    (2, 3, 5),
    (2, 4, 5),
]

ADJACENT_LEG_TRIOS = [
    (0, 1, 2),
    (1, 2, 3),
    (2, 3, 4),
    (3, 4, 5),
    (0, 4, 5),
    (0, 1, 5),
]

LEG_TRIOS = SOME_LEG_TRIOS + ADJACENT_LEG_TRIOS


# math.stackexchange.com/questions/544946/
#   determine-if-projection-of-3d-point-onto-plane-is-within-a-triangle
# gamedev.stackexchange.com/questions/23743/
#   whats-the-most-efficient-way-to-find-barycentric-coordinates
# en.wikipedia.org/wiki/Barycentric_coordinate_system
def is_stable(p1, p2, p3, tol=0.001):
    """
    Determines stability of the pose.
    Determine if projection of 3D point p
    onto the plane defined by p1, p2, p3
    is within a triangle defined by p1, p2, p3.
    """
    p = Vector(0, 0, 0)
    u = vector_from_to(p1, p2)
    v = vector_from_to(p1, p3)
    n = cross(u, v)
    w = vector_from_to(p1, p)
    n2 = dot(n, n)
    beta = dot(cross(u, w), n) / n2
    gamma = dot(cross(w, v), n) / n2
    alpha = 1 - gamma - beta
    # then coordinate of the projected point (p_) of point p
    # p_ = alpha * p1 + beta * p2 + gamma * p3
    min_val = -tol
    max_val = 1 + tol
    cond1 = min_val <= alpha <= max_val
    cond2 = min_val <= beta <= max_val
    cond3 = min_val <= gamma <= max_val
    return cond1 and cond2 and cond3


def is_lower(point, height, n, tol=1):
    _height = -dot(n, point)
    return _height > height + tol


def find_legs_on_ground(legs, n, height, tol=1):
    legs_on_ground = []
    for leg in legs:
        for point in reversed(leg.all_points[1:]):
            _height = -dot(n, point)
            if isclose(height, _height, abs_tol=tol):
                legs_on_ground.append(leg)
                break

    return legs_on_ground
