from hexapod.models import VirtualHexapod
from hexapod.ik_solver.ik_solver import inverse_kinematics_update
from tests.ik_cases.case1 import given_dimensions, given_ik_parameters, correct_poses
from tests.helpers import assert_poses_equal


def test_sample_ik():
    hexapod = VirtualHexapod(given_dimensions)
    _, result_poses = inverse_kinematics_update(hexapod, given_ik_parameters)
    assert_poses_equal(result_poses, correct_poses)
