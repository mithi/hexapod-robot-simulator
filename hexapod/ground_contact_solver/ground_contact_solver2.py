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
        (height, n_axis, 3 ground contacts)
"""
from math import isclose
from itertools import combinations
from hexapod.ground_contact_solver.helpers import is_stable
from hexapod.points import get_normal_given_three_points, dot

TOL = 1.0


def all_joint_id_combinations():
    joints_combination_list = []
    # joint coxia point 1, femur point 2, foot_tip 3
    for i in range(3, 0, -1):
        for j in range(3, 0, -1):
            for k in range(3, 0, -1):
                joints_combination_list.append([i, j, k])

    return joints_combination_list


other_points_map = {1: [2, 3], 2: [3, 1], 3: [1, 2]}


def compute_orientation_properties(legs):
    leg_trios = list(combinations(range(6), 3))
    joint_trios = all_joint_id_combinations()

    for leg_trio, other_leg_trio in zip(leg_trios, reversed(leg_trios)):

        three_legs = [legs[i] for i in leg_trio]
        other_three_legs = [legs[i] for i in other_leg_trio]

        for joint_trio in joint_trios:

            p0, p1, p2 = [legs[i].get_point(j) for i, j in zip(leg_trio, joint_trio)]

            if not is_stable(p0, p1, p2):
                continue

            n = get_normal_given_three_points(p0, p1, p2)
            height = -dot(n, p0)

            if same_leg_joints_break_condition(three_legs, joint_trio, height, n):
                continue

            if other_leg_joints_break_condition(other_three_legs, height, n):
                continue

            legs_on_ground = find_legs_on_ground(legs, height, n)
            return legs_on_ground, n, height

    return [], None, None


def other_leg_joints_break_condition(other_three_legs, height, n):
    for leg in other_three_legs:
        for i_ in range(1, 4):
            height_to_test = -dot(n, leg.get_point(i_))
            if height_to_test > height + TOL:
                return True
    return False


def same_leg_joints_break_condition(three_legs, three_point_ids, height, n):
    for leg, point_id in zip(three_legs, three_point_ids):
        for other_point_id in other_points_map[point_id]:
            other_point = leg.get_point(other_point_id)
            height_to_test = -dot(n, other_point)
            if height_to_test > height + TOL:
                return True
    return False


def find_legs_on_ground(legs, height, n):
    legs_on_ground = []
    for leg in legs:
        for point in reversed(leg.all_points[1:]):
            _height = -dot(n, point)
            if isclose(height, _height, abs_tol=TOL):
                legs_on_ground.append(leg)
                break

    return legs_on_ground
