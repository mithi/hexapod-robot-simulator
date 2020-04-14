from copy import deepcopy
from hexapod.models import VirtualHexapod, Hexagon
from hexapod.points import (
    angle_between,
    is_counter_clockwise,
    Point,
    rotz,
    vector_from_to,
    length,
)
from settings import ASSERTION_ENABLED, PRINT_IK
import numpy as np


def recompute_hexapod(dimensions, ik_parameters, poses):

    old_hexapod = VirtualHexapod(dimensions)
    old_hexapod.update_stance(ik_parameters["hip_stance"], ik_parameters["leg_stance"])
    old_contacts = deepcopy(old_hexapod.ground_contacts)

    new_hexapod = VirtualHexapod(dimensions)
    new_hexapod.update(poses)
    new_contacts = deepcopy(new_hexapod.ground_contacts)

    id1, id2 = find_two_same_leg_ids(old_contacts, new_contacts)

    old_p1 = deepcopy(old_hexapod.legs[id1].ground_contact())
    old_p2 = deepcopy(old_hexapod.legs[id2].ground_contact())
    new_p1 = deepcopy(new_hexapod.legs[id1].ground_contact())
    new_p2 = deepcopy(new_hexapod.legs[id2].ground_contact())

    old_vector = vector_from_to(old_p1, old_p2)
    new_vector = vector_from_to(new_p1, new_p2)

    translate_vector = vector_from_to(new_p1, old_p1)
    _, twist_frame = find_twist_to_recompute_hexapod(new_vector, old_vector)
    new_hexapod.rotate_and_shift(twist_frame, 0)

    twisted_p2 = new_hexapod.legs[id2].p3
    translate_vector = vector_from_to(twisted_p2, old_p2)
    new_hexapod.move_xyz(translate_vector.x, translate_vector.y, 0)

    might_sanity_check_points(new_p1, new_p2, old_p1, old_p2, new_vector, old_vector)

    return new_hexapod


def make_contact_dict(ground_contact_list):
    # map index in ground_contact_list
    contact_dict = {}
    for contact in ground_contact_list:
        left_or_right, front_mid_back, _ = contact.name.split("-")
        leg_placement = left_or_right + "-" + front_mid_back
        leg_id = Hexagon.VERTEX_NAMES.index(leg_placement)
        contact_dict[leg_id] = leg_placement

    return contact_dict


def find_two_same_leg_ids(old_contacts, new_contacts):
    same_ids = []
    old_contact_dict = make_contact_dict(old_contacts)
    new_contact_dict = make_contact_dict(new_contacts)

    if PRINT_IK:
        print("In recomputing hexapod:")
        print("...old contacts:", old_contact_dict)
        print("...new_contacts: ", old_contact_dict)

    for leg_id in old_contact_dict.keys():
        if leg_id not in new_contact_dict.keys():
            continue

        same_ids.append(leg_id)
        if len(same_ids) == 2:
            return same_ids[0], same_ids[1]

    raise Exception(
        f"No same points on ground. \n old: {old_contact_dict} \n new: {new_contact_dict}"
    )


def find_twist_to_recompute_hexapod(a, b):
    twist = angle_between(a, b)
    z_axis = Point(0, 0, -1)
    is_ccw = is_counter_clockwise(a, b, z_axis)
    if is_ccw:
        twist = -twist

    twist_frame = rotz(twist)
    return twist, twist_frame


def might_sanity_check_points(new_p1, new_p2, old_p1, old_p2, new_vector, old_vector):
    if not ASSERTION_ENABLED:
        return

    print("Sanity check on recompute hexapod")
    assert np.isclose(new_p1.z, 0, atol=1.0), f"Point should be on the ground:\n{new_p1}"
    assert np.isclose(new_p2.z, 0, atol=1.0), f"Point should be on the ground:\n{new_p2}"
    assert np.isclose(old_p1.z, 0, atol=1.0), f"Point should be on the ground:\n{old_p1}"
    assert np.isclose(old_p2.z, 0, atol=1.0), f"Point should be on the ground:\n{old_p2}"
    assert new_p1.name == old_p1.name, f"Should be the same name:\n{old_p1}\n{new_p1}"
    assert new_p2.name == old_p2.name, f"Should be the same name:\n{old_p2}\n{new_p2}"
    assert np.isclose(
        length(new_vector), length(old_vector), atol=1.0
    ), f"Should be same length.\nnew_vector:{new_vector}\n old_vector{old_vector}"
