from settings import (
    PRINT_IK_LOCAL_LEG,
    PRINT_IK,
    BETA_MAX_ANGLE,
    GAMMA_MAX_ANGLE,
)
import json
import numpy as np
from hexapod.points import length, vector_from_to


def body_contact_shoved_on_ground(hexapod):
    for i in range(hexapod.LEG_COUNT):
        body_contact = hexapod.body.vertices[i]
        foot_tip = hexapod.legs[i].foot_tip()
        if body_contact.z < foot_tip.z:
            return True
    return False


def legs_too_short(legs):
    # True when
    # if three of her left legs are up or
    # if three of her right legs are up or
    # if four legs are up
    if len(legs) >= 4:
        return True, f"Unstable. Too many legs off the floor. \n {legs}"

    if len(legs) == 3:
        leg_positions = [leg.split("-")[0] for leg in legs]
        if leg_positions.count("left") == 3:
            return True, f"Unstable. All left legs off the ground. \n {legs}"
        if leg_positions.count("right") == 3:
            return True, f"Unstable. All right legs off the ground. \n {legs}"

    return False, None


def angle_above_limit(angle, angle_range, leg_name, angle_name):
    if np.abs(angle) > angle_range:
        return (
            True,
            f"The {angle_name} (of {leg_name} leg) required \n \
      to do this pose is above the range of motion. \n \
      Required: {angle} degrees. Limit: {angle_range} degrees.",
        )

    return False, None


def beta_gamma_not_within_range(beta, gamma, leg_name):
    beta_limit, alert_msg = angle_above_limit(
        beta, BETA_MAX_ANGLE, leg_name, "beta angle (beta)"
    )
    if beta_limit:
        return True, alert_msg

    gamma_limit, alert_msg = angle_above_limit(
        gamma, GAMMA_MAX_ANGLE, leg_name, "gamma angle (gamma)"
    )
    if gamma_limit:
        return True, alert_msg

    return False, None


def might_print_ik(poses, ik_parameters, hexapod):
    if not PRINT_IK:
        return

    print("█████████████████████████████")
    print("█ START INVERSE KINEMATICS  █")
    print("█████████████████████████████")

    print(".....................")
    print("... ik_parameters: ")
    print(".....................")

    print(json.dumps(ik_parameters, indent=4))

    print(".....................")
    print("... poses: ")
    print(".....................")

    print(json.dumps(poses, indent=4))

    print(".....................")
    print("... hexapod: ")
    print(".....................")

    hexapod.print()
    print("█████████████████████████████")
    print("█ END INVERSE KINEMATICS    █")
    print("█████████████████████████████")


def sanity_leg_lengths_check(hexapod, leg_name, points):
    coxia = length(vector_from_to(points[0], points[1]))
    femur = length(vector_from_to(points[1], points[2]))
    tibia = length(vector_from_to(points[2], points[3]))

    assert np.isclose(
        hexapod.coxia, coxia, atol=1
    ), f"wrong coxia vector length. {leg_name} coxia:{coxia}"
    assert np.isclose(
        hexapod.femur, femur, atol=1
    ), f"wrong femur vector length. {leg_name} femur:{femur}"
    assert np.isclose(
        hexapod.tibia, tibia, atol=1
    ), f"wrong tibia vector length. {leg_name} tibia:{tibia}"


def might_print_points(points, leg_name):
    if not PRINT_IK_LOCAL_LEG:
        return

    print()
    print(leg_name, "leg")
    print(f"...p0: {points[0]}")
    print(f"...p1: {points[1]}")
    print(f"...p2: {points[2]}")
    print(f"...p3: {points[3]}")
    print()
