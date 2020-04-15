from hexapod.models import VirtualHexapod
import hexapod.ik_solver.ik_solver2 as ik_solver2
import hexapod.ik_solver.ik_solver as ik_solver

from tests.ik_cases.case1 import given_dimensions, given_ik_parameters, correct_poses
from tests.helpers import assert_poses_equal


def assert_ik_solver(ik_function):
    hexapod = VirtualHexapod(given_dimensions)
    result_poses, hexapod = ik_function(hexapod, given_ik_parameters)
    assert_poses_equal(result_poses, correct_poses)


def test_sample_ik():
    assert_ik_solver(ik_solver2.inverse_kinematics_update)
    assert_ik_solver(ik_solver.inverse_kinematics_update)
