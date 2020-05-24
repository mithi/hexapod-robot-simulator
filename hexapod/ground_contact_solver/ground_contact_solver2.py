"""
❗❗❗This is a more general algorithm to account for the cases
that are not handled correctly by the other ground_contact_solver.
This will only be used by the kinematics-page of the app.
This algorithm can be optimized or replaced if a more elegant
algorithm is available.
❗❗❗

We have 18 points total.
(6 legs, three possible points per leg)

We have a total of 540 combinations
- get three legs out of six (20 combinations)
  - we have three possible points for each leg, that's 27 (3^3)
  -  27 * 20 is 540

For each combination:
    1. Check if stable if not, next
      - Check if the projection of the center of gravity to the plane
        defined by the three points lies inside the triangle, if not, next
    2. Get the height and normal of the height and normal of the triangle plane
        (We need this for the next part)
    3. For each of the three leg, check if the two other points on the leg is not a
        lower height, if condition if broken, next. (6 points total)
    4. For each of the three other legs, check all points (3 points of each leg)
        if so, next. (9 points total)
    5. If no condition is violated, then this is good, return this!
"""
import random
from hexapod.ground_contact_solver.shared import (
    is_stable,
    is_lower,
    find_legs_on_ground,
    SOME_LEG_TRIOS,
    ADJACENT_LEG_TRIOS,
)
from hexapod.points import get_normal_given_three_points, dot

OTHER_POINTS_MAP = {1: (2, 3), 2: (3, 1), 3: (1, 2)}

JOINT_TRIOS = []
for i in range(3, 0, -1):
    for j in range(3, 0, -1):
        for k in range(3, 0, -1):
            JOINT_TRIOS.append((i, j, k))


def compute_orientation_properties(legs):
    """
    Returns:
      - Which legs are on the ground
      - Normal vector of the plane defined by these legs
      - Distance of this plane to center of gravity
    """
    # prefer leg combinations where legs are not adjacent to each other
    # introduce some randomness so we are not bias in
    # choosing one stable position over another
    shuffled_some_leg_trios = random.sample(SOME_LEG_TRIOS, len(SOME_LEG_TRIOS))
    leg_trios = shuffled_some_leg_trios + ADJACENT_LEG_TRIOS

    for leg_trio in leg_trios:

        other_leg_trio = [i for i in range(6) if i not in leg_trio]
        other_three_legs = [legs[i] for i in other_leg_trio]
        three_legs = [legs[i] for i in leg_trio]

        for joint_trio in JOINT_TRIOS:

            p0, p1, p2 = [legs[i].get_point(j) for i, j in zip(leg_trio, joint_trio)]

            if not is_stable(p0, p1, p2):
                continue

            n = get_normal_given_three_points(p0, p1, p2)
            height = -dot(n, p0)

            if same_leg_joints_break_condition(three_legs, joint_trio, n, height):
                continue

            if other_leg_joints_break_condition(other_three_legs, n, height):
                continue

            legs_on_ground = find_legs_on_ground(legs, n, height)
            return legs_on_ground, n, height

    return [], None, None


def same_leg_joints_break_condition(three_legs, three_point_ids, n, height):
    for leg, point_id in zip(three_legs, three_point_ids):
        for other_point_id in OTHER_POINTS_MAP[point_id]:
            point = leg.get_point(other_point_id)
            if is_lower(point, height, n):
                return True
    return False


def other_leg_joints_break_condition(other_three_legs, n, height):
    for leg in other_three_legs:
        for point in leg.all_points[1:]:
            if is_lower(point, height, n):
                return True
    return False
