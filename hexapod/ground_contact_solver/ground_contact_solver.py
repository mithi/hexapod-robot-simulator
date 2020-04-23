"""
❗❗❗An algorithm for computing the robot's orientation
assuming probably ground contacts are known.

This algorithm rests upon the assumption that it
knows which point of the each leg is in contact with the ground.
This assumption seems to be true for all possible cases for
leg-patterns page and inverse-kinematics page.

But this is not true for all possible
angle combinations (18 angles) that can be defined in
the kinematics page.

This module is used for the leg-patterns page,
and the inverse-kinematics page.

The other module will be used for the kinematics page.
❗❗❗

This module is responsible for the following:
1. determining which legs of the hexapod is on the ground
2. Computing the normal vector of the triangle defined by at least three legs on the ground
the normal vector wrt to the old normal vector that is defined by the legs on the ground in
the hexapod's neutral position
3. Determining the height of the center of gravity (cog) wrt to the ground.
ie this height is distance between the cog and the plane defined by ground contacts.
"""
from hexapod.points import dot, get_normal_given_three_points
from hexapod.ground_contact_solver.shared import (
    is_stable,
    is_lower,
    find_legs_on_ground,
    LEG_TRIOS,
)


def compute_orientation_properties(legs):
    """
    Returns:
      - Which legs are on the ground
      - Normal vector of the plane defined by these legs
      - Distance of this plane to center of gravity
    """
    n, height = find_ground_plane_properties(legs)

    # this pose is unstable, The hexapod has no balance
    if n is None:
        return [], None, None

    return find_legs_on_ground(legs, n, height), n, height


def find_ground_plane_properties(legs):
    """
    Return three legs forming a stable position from legs,
    or None if no three legs satisfy this requirement.
    It also returns the normal vector of the plane
    defined by the three ground contacts, and the
    computed distance of the hexapod body to the ground plane
    """
    ground_contacts = [leg.ground_contact() for leg in legs]

    # (2, 3, 5) is a trio from the set [0, 1, 2, 3, 4, 5]
    # the corresponding other_trio of (2, 3, 5) is (0, 1, 4)
    # order is not important ie (2, 3, 5) is the same as (5, 3, 2)
    for trio in LEG_TRIOS:
        p0, p1, p2 = [ground_contacts[i] for i in trio]

        if not is_stable(p0, p1, p2):
            continue

        # Get the vector normal to plane defined by these points
        # ❗IMPORTANT: The normal is always pointing up
        # because of how we specified the order of the trio
        # (and the legs in general)
        # starting from middle-right (id:0) to right back (id:5)
        # always towards one direction (ccw)
        n = get_normal_given_three_points(p0, p1, p2)

        # p0 is vector from cog (0, 0, 0) to ground contact
        # dot product of this and normal we get the
        # hypothetical (negative) height of ground contact to cog
        #
        #  cog *  ^ (normal_vector) ----
        #      \  |                  |
        #       \ |               -height
        #        \|                  |
        #         V p0 (foot_tip) ------
        #
        # using p0, p1 or p2 should yield the same result
        height = -dot(n, p0)

        # height should be the highest since
        # the plane defined by this trio is on the ground
        # the other legs ground contact cannot be lower than the ground
        other_trio = [i for i in range(6) if i not in trio]
        other_points = [ground_contacts[i] for i in other_trio]
        if no_other_legs_lower(n, height, other_points):
            # Found one!
            return n, height

    # Nothing met the condition
    return None, None


def no_other_legs_lower(n, height, other_points):
    for point in other_points:
        if is_lower(point, height, n):
            return False

    return True
