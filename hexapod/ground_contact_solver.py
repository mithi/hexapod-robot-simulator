#
# This module is responsible for the following:
# 1. determining which legs of the hexapod is on the ground
# 2. Computing the normal vector of the triangle defined by at least three legs on the ground
# the normal vector wrt to the old normal vector that is defined by the legs on the ground in
# the hexapod's neutral position
# 3. Determining the height of the center of gravity wrt to the ground
#
import numpy as np
from itertools import combinations
from .points import Point, dot, get_unit_normal, is_point_inside_triangle


def get_legs_on_ground(legs):
    def within_thresh(a, b, tol=2):
        return np.abs(a - b) < tol

    trio = three_ids_of_ground_contacts(legs)

    # This pose is unstable, The hexapod has no balance
    if trio is None:
        return [], None, None

    p0, p1, p2 = get_corresponding_ground_contacts(trio, legs)
    n = get_unit_normal(p0, p1, p2)

    # Note: using p0, p1 or p2 should yield the same result
    cog_from_ground = -dot(n, p0)

    legs_on_ground = []

    # Get all contacts of the same height
    for leg in legs:
        ground_contact = -dot(n, leg.ground_contact())
        if within_thresh(ground_contact, cog_from_ground):
            legs_on_ground.append(leg)

    return legs_on_ground, n, cog_from_ground


# This function takes the legs of the hexapod
# and finds three legs on the ground that form a stable position
# returns the leg ids of those three legs
# return None if no stable position found
def three_ids_of_ground_contacts(legs):
    trios, other_trios = set_of_two_trios_from_six()

    for trio, other_trio in zip(trios, other_trios):
        # Let p0 to p6 be leg ground contacts
        p0, p1, p2 = get_corresponding_ground_contacts(trio, legs)

        if check_stability(p0, p1, p2) == True:
            # The vector normal to plane defined by these points
            # ❗IMPORTANT: Normal is always pointing up
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
            p3, p4, p5 = get_corresponding_ground_contacts(other_trio, legs)
            for p in [p3, p4, p5]:
                h_ = dot(n, p)

                # Wrong leg combination, check another
                if h_ < h:
                    condition_violated = True
                    break

            if condition_violated:
                continue
            else:
                #  Found one!
                return trio

    # Nothing met the condition
    return None


# Given the three leg ids and the list of legs
# get the points contacting the ground of those three legs
def get_corresponding_ground_contacts(ids, legs):
    i, j, k = ids
    return legs[i].ground_contact(), legs[j].ground_contact(), legs[k].ground_contact()


# Get all combinations of a three-item-group given six items
# 20 combinations total
# (2, 3, 5) is a trio from set [0, 1, 2, 3, 4, 5]
# the corresponding other_trio of (2, 3, 5) is (0, 1, 4)
# order is not important ie (2, 3, 5) is the same as (5, 3, 2)
def set_of_two_trios_from_six():
    trios = [trio for trio in combinations(range(6), 3)]
    other_trios = []

    for trio in trios:
        other_trio = [i for i in filter(lambda x: x not in trio, range(6))]
        other_trios.append(other_trio)

    return trios, other_trios


# If the center of gravity p (0, 0) on xy plane
# is inside projection (in the xy plane) of
# the triangle defined by point a, b, c, then this is stable
def check_stability(a, b, c):
    p = Point(0, 0, 0)
    return is_point_inside_triangle(p, a, b, c)
