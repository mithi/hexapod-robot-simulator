from hexapod.models import VirtualHexapod
import hexapod.ik_solver.ik_solver2 as ik_solver2
import hexapod.ik_solver.ik_solver as ik_solver

from tests.ik_cases.case1 import given_dimensions, given_ik_parameters, correct_poses
from tests.helpers import assert_poses_equal


def test_sample_ik():
    hexapod = VirtualHexapod(given_dimensions)
    result_poses, hexapod = ik_solver.inverse_kinematics_update(hexapod, given_ik_parameters)
    assert_poses_equal(result_poses, correct_poses)

def test_sample_ik2():
    hexapod = VirtualHexapod(given_dimensions)
    result_poses, hexapod = ik_solver2.inverse_kinematics_update(hexapod, given_ik_parameters)
    assert_poses_equal(result_poses, correct_poses)
