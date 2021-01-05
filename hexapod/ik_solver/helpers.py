# Used for checking edge cases
# and also for printing final results
import json
import numpy as np
from settings import (
    PRINT_IK_LOCAL_LEG,
    ASSERTION_ENABLED,
    PRINT_IK,
    BETA_MAX_ANGLE,
    GAMMA_MAX_ANGLE,
)
from hexapod.points import length, vector_from_to, angle_between

COXIA_ON_GROUND_ALERT_MSG = "Impossible at given height.\ncoxia joint shoved on ground"
BODY_ON_GROUND_ALERT_MSG = "Impossible at given height.\nbody contact shoved on ground"


def cant_reach_alert_msg(leg_name, problem):
    msg = "Cannot reach target ground point.\n"
    if problem == "femur":
        msg += f"Femur length of {leg_name} leg is too long."
    if problem == "tibia":
        msg += f"Femur length of {leg_name} leg is too long."
    else:
        # blocking
        msg = f"The {leg_name} leg cannot reach it because the ground is blocking the path."
    return msg


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
        return True, f"Unstable. Too many legs off the floor.\n{legs}"

    leg_positions = [leg.split("-")[0] for leg in legs]
    if leg_positions.count("left") == 3:
        return True, f"Unstable. All left legs off the ground.\n{legs}"
    if leg_positions.count("right") == 3:
        return True, f"Unstable. All right legs off the ground.\n{legs}"

    return False, None


def angle_above_limit(angle, angle_range, leg_name, angle_name):
    if np.abs(angle) > angle_range:
        alert_msg = f"The {angle_name} (of {leg_name} leg) required\n\
            to do this pose is beyond the range of motion.\n\
            Required: {angle} degrees. Limit: {angle_range} degrees."
        return True, alert_msg

    return False, None


def beta_gamma_not_in_range(beta, gamma, leg_name):
    limit, msg = angle_above_limit(beta, BETA_MAX_ANGLE, leg_name, "(beta/femur)")
    if limit:
        return True, msg

    limit, msg = angle_above_limit(gamma, GAMMA_MAX_ANGLE, leg_name, "(gamma/tibia)")
    if limit:
        return True, msg

    return False, None


def wrong_length_msg(leg_name, limb_name, limb_value):
    return f"Wrong {limb_name} vector length. {leg_name} coxia:{limb_value}"


def might_sanity_leg_lengths_check(hexapod, leg_name, points):
    if not ASSERTION_ENABLED:
        return

    coxia = length(vector_from_to(points[0], points[1]))
    femur = length(vector_from_to(points[1], points[2]))
    tibia = length(vector_from_to(points[2], points[3]))

    same_length = np.isclose(hexapod.coxia, coxia, atol=1)
    assert same_length, wrong_length_msg(leg_name, "coxia", coxia)

    same_length = np.isclose(hexapod.femur, femur, atol=1)
    assert same_length, wrong_length_msg(leg_name, "femur", femur)

    same_length = np.isclose(hexapod.tibia, tibia, atol=1)
    assert same_length, wrong_length_msg(leg_name, "tibia", tibia)


def might_sanity_beta_gamma_check(beta, gamma, leg_name, points):
    if not ASSERTION_ENABLED:
        return

    coxia = vector_from_to(points[0], points[1])
    femur = vector_from_to(points[1], points[2])
    tibia = vector_from_to(points[2], points[3])
    result_beta = angle_between(coxia, femur)

    same_beta = np.isclose(np.abs(beta), result_beta, atol=1)
    assert same_beta, f"{leg_name} leg: expected: |{beta}|, found: {result_beta}"

    # ❗IMPORTANT: Sometimes both are zero. Is this wrong?
    femur_tibia_angle = angle_between(femur, tibia)
    is_90 = np.isclose(90, femur_tibia_angle + gamma, atol=1)

    if not is_90:
        alert_msg = f"{leg_name} leg:\
            {femur_tibia_angle} (femur-tibia angle) + {gamma} (gamma) != 90."
        print(alert_msg)


def might_print_ik(poses, ik_parameters, hexapod):
    if not PRINT_IK:
        return

    print("█████████████████████████████")
    print("█ START INVERSE KINEMATICS  █")
    print("█████████████████████████████")

    print(".....................")
    print("... hexapod dimensions: ")
    print(".....................")
    print(json.dumps(hexapod.dimensions, indent=4))

    print(".....................")
    print("... ik parameters: ")
    print(".....................")
    print(json.dumps(ik_parameters, indent=4))

    print(".....................")
    print("... poses: ")
    print(".....................")
    print(json.dumps(poses, indent=4))

    print("█████████████████████████████")
    print("█ END INVERSE KINEMATICS    █")
    print("█████████████████████████████")


def might_print_points(points, leg_name):
    if not PRINT_IK_LOCAL_LEG:
        return

    print(leg_name, "leg")
    for i, point in enumerate(points):
        print(f"...p{i}: {point}")
    print()
