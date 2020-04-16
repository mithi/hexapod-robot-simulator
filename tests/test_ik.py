from copy import deepcopy
from hexapod.models import VirtualHexapod
import hexapod.ik_solver.ik_solver2 as ik_solver2
import hexapod.ik_solver.ik_solver as ik_solver

from tests.ik_cases import case1, case2
from tests.helpers import assert_poses_equal, assert_two_hexapods_equal

CASES = [case1, case2]


def assert_ik_solver(ik_function, case):
    hexapod = VirtualHexapod(case.given_dimensions)
    result_poses, _ = ik_function(hexapod, case.given_ik_parameters)
    assert_poses_equal(result_poses, case.correct_poses, case.description)


def test_sample_ik():
    for case in CASES:
        assert_ik_solver(ik_solver2.inverse_kinematics_update, case)
        assert_ik_solver(ik_solver.inverse_kinematics_update, case)
        assert_ik_solver(ik_solver2.inverse_kinematics_update, case)
        assert_ik_solver(ik_solver.inverse_kinematics_update, case)


def test_points_ik2():
    for case in CASES:
        hexapod = VirtualHexapod(case.given_dimensions)
        hexapod_ik = deepcopy(hexapod)
        hexapod_k = deepcopy(hexapod)

        poses, _ = ik_solver2.inverse_kinematics_update(
            hexapod, case.given_ik_parameters
        )

        hexapod_ik.update(poses)
        hexapod_k.update(case.correct_poses)

        assert_two_hexapods_equal(hexapod_ik, hexapod_k, case.description)
