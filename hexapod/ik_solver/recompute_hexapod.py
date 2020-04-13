from copy import deepcopy
from hexapod.models import VirtualHexapod
from hexapod.points import (
    angle_between,
    is_counter_clockwise,
    Point,
    rotz,
    vector_from_to,
    length,
)
from settings import ASSERTION_ENABLED
import numpy as np


def recompute_hexapod(dimensions, ik_parameters, poses):
    # ❗❗IMPORTANT!This assumes leg with id 3 and id 4 are on the ground
    # THIS IS NOT ALWAYS THE CASE.
    # Should check which two legs are both on the ground before and after
    # instead of using leg 3 and 4
    old_hexapod = VirtualHexapod(dimensions)
    old_hexapod.update_stance(ik_parameters["hip_stance"], ik_parameters["leg_stance"])
    old_p1 = deepcopy(old_hexapod.legs[3].p3)
    old_p2 = deepcopy(old_hexapod.legs[4].p3)
    old_vector = vector_from_to(old_p1, old_p2)

    new_hexapod = VirtualHexapod(dimensions)
    new_hexapod.update(poses)
    new_p1 = deepcopy(new_hexapod.legs[3].p3)
    new_p2 = deepcopy(new_hexapod.legs[4].p3)
    new_vector = vector_from_to(new_p1, new_p2)

    translate_vector = vector_from_to(new_p1, old_p1)
    _, twist_frame = find_twist_to_recompute_hexapod(new_vector, old_vector)
    new_hexapod.rotate_and_shift(twist_frame, 0)
    twisted_p2 = new_hexapod.legs[4].p3
    translate_vector = vector_from_to(twisted_p2, old_p2)
    new_hexapod.move_xyz(translate_vector.x, translate_vector.y, 0)

    if ASSERTION_ENABLED:
        assert np.isclose(new_p1.z, 0)
        assert np.isclose(new_p2.z, 0)
        assert np.isclose(old_p1.z, 0, atol=0.1)
        assert np.isclose(old_p2.z, 0, atol=0.1)
        assert new_p1.name == old_p1.name
        assert new_p2.name == old_p2.name
        assert np.isclose(length(new_vector), length(old_vector), atol=0.1)

    return new_hexapod


def find_twist_to_recompute_hexapod(a, b):
    twist = angle_between(a, b)
    z_axis = Point(0, 0, -1)
    is_ccw = is_counter_clockwise(a, b, z_axis)
    if is_ccw:
        twist = -twist

    twist_frame = rotz(twist)
    return twist, twist_frame
