from copy import deepcopy
from hexapod.const import BASE_DIMENSIONS
from hexapod.models import VirtualHexapod
from hexapod.points import Vector
from hexapod.ik_solver import ik_solver, ik_solver2
from hexapod.ik_solver.shared import update_hexapod_points

from tests.ik_cases import case1, case2, case3
from tests.helpers import assert_poses_equal, assert_two_hexapods_equal

CASES = [case1, case2, case3]


def assert_ik_solver(ik_function, case):
    hexapod = VirtualHexapod(case.given_dimensions)
    result_poses, _ = ik_function(hexapod, case.given_ik_parameters)
    assert_poses_equal(result_poses, case.correct_poses, case.description)


def assert_ik_points(case, assume_ground_targets):
    hexapod = VirtualHexapod(case.given_dimensions)
    hexapod_ik = deepcopy(hexapod)
    hexapod_k = deepcopy(hexapod)

    poses, _ = ik_solver2.inverse_kinematics_update(hexapod, case.given_ik_parameters)

    hexapod_ik.update(poses, assume_ground_targets)
    hexapod_k.update(case.correct_poses, assume_ground_targets)

    assert_two_hexapods_equal(hexapod_ik, hexapod_k, case.description)


def test_sample_ik():
    for case in CASES:
        assert_ik_solver(ik_solver2.inverse_kinematics_update, case)
        assert_ik_solver(ik_solver.inverse_kinematics_update, case)
        assert_ik_solver(ik_solver2.inverse_kinematics_update, case)
        assert_ik_solver(ik_solver.inverse_kinematics_update, case)


def test_points_ik2_assume_ground_targets():
    for case in CASES:
        assert_ik_points(case, True)


def test_points_ik2_dont_assume_ground_targets():
    for case in CASES:
        assert_ik_points(case, False)


def test_shared_set_points():
    points = [
        Vector(1, 2, 3, "a"),
        Vector(1, 2, 3, "b"),
        Vector(1, 2, 3, "c"),
        Vector(1, 2, 3, "d"),
    ]

    vh = VirtualHexapod(BASE_DIMENSIONS)
    update_hexapod_points(vh, 1, points)
    for leg_point, point in zip(vh.legs[1].all_points, points):
        assert leg_point is point
