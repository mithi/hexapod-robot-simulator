"""
This module is responsible for the following:
1. determining which legs of the hexapod is on the ground
2. Computing the normal vector of the triangle defined by at least three legs on the ground
the normal vector wrt to the old normal vector that is defined by the legs on the ground in
the hexapod's neutral position
3. Determining the height of the center of gravity wrt to the ground
"""

from itertools import combinations
from hexapod.points import Point, dot, get_unit_normal, is_point_inside_triangle
from math import isclose


def get_legs_on_ground(legs):
    trio = three_ids_of_ground_contacts(legs)

    # This pose is unstable, The hexapod has no balance
    if trio is None:
        return [], None, None

    p0, p1, p2 = get_corresponding_ground_contacts(trio, legs)
    n = get_unit_normal(p0, p1, p2)

    # Note: using p0, p1 or p2 should yield the same result
    # height from cog to ground
    height = -dot(n, p0)

    legs_on_ground = []

    # Get all contacts of the same height
    for leg in legs:
        _height = -dot(n, leg.ground_contact())
        if isclose(height, _height, abs_tol=1):
            legs_on_ground.append(leg)

    return legs_on_ground, n, height


def three_ids_of_ground_contacts(legs, tol=1):
    """
    Return three legs forming a stable position from legs,
    or None if no three legs satisfy this requirement.

    This function takes the legs of the hexapod
    and finds three legs on the ground that form a stable position
    returns the leg ids of those three legs
    return None if no stable position found
    """
    trios = set_of_two_trios_from_six()
    ground_contacts = [leg.ground_contact() for leg in legs]
    for trio, other_trio in zip(trios, reversed(trios)):
        p0 = ground_contacts[trio[0]]
        p1 = ground_contacts[trio[1]]
        p2 = ground_contacts[trio[2]]
        # Let p0 to p5 be leg ground contacts
        if not check_stability(p0, p1, p2):
            continue

        # Get the vector normal to plane defined by these points
        # ❗IMPORTANT: The Normal is always pointing up
        # because of how we specified the order of the trio
        # (and the legs in general)
        # starting from middle-right (id:0) to right back (id:5)
        # always towards one direction (ccw)
        n = get_unit_normal(p0, p1, p2)

        # p0 is vector from cog (0, 0, 0) to ground contact
        # dot product of this and normal we get the
        # hypothetical (negative) height of ground contact to cog
        #
        #  cog *  ^ (normal_vector) ----
        #      \  |                  |
        #       \ |                 height
        #        \|                  |
        #         V p0 (foot_tip) ---V---
        #
        # using p0, p1 or p2 should yield the same result
        h = dot(n, p0)

        # h should be the most negative(the lowest) since
        # the plane defined by this trio is on the ground
        # the other legs ground contact cannot be lower than the ground
        condition_violated = False
        for p in other_trio:
            if dot(n, ground_contacts[p]) + tol < h:
                # Wrong leg combination, check another
                condition_violated = True
                break

        if not condition_violated:
            return trio  # Found one!

    # Nothing met the condition
    return None


def get_corresponding_ground_contacts(ids, legs):
    """
    Given three leg ids and the list of legs get the points
    contacting the ground of those three legs.
    """
    i, j, k = ids
    return legs[i].ground_contact(), legs[j].ground_contact(), legs[k].ground_contact()


def set_of_two_trios_from_six():
    """
    Get all combinations of a three-item-group given six items.

    20 combinations total
    (2, 3, 5) is a trio from set [0, 1, 2, 3, 4, 5]
    the corresponding other_trio of (2, 3, 5) is (0, 1, 4)
    order is not important ie (2, 3, 5) is the same as (5, 3, 2)
    """
    return list(combinations(range(6), 3))


def check_stability(a, b, c):
    """
    Check if the points a, b, c form a stable triangle.

    If the center of gravity p (0, 0) on xy plane
    is inside projection (in the xy plane) of
    the triangle defined by point a, b, c, then this is stable
    """
    return is_point_inside_triangle(Point(0, 0, 0), a, b, c)
