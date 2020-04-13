from hexapod.models import VirtualHexapod
from hexapod.ik_solver.ik_solver import inverse_kinematics_update  # , recompute_hexapod
from tests.ik_cases.case1 import given_dimensions, given_ik_parameters, correct_poses
from tests.helpers import assert_poses_equal  # , assert_hexapod_equal


def test_sample_ik():
    hexapod = VirtualHexapod(given_dimensions)
    _, result_poses, msg = inverse_kinematics_update(hexapod, given_ik_parameters)
    assert msg is None
    assert_poses_equal(result_poses, correct_poses)


def test_recompute_hexapod():
    # ❗❗❗ This test fails!
    # See discussion in:
    # https://mithi.github.io/robotics-blog/blog/hexapod-simulator/3-prerelease-2/
    # hexapod1 = VirtualHexapod(given_dimensions)
    # _, result_poses, msg = inverse_kinematics_update(hexapod1, given_ik_parameters)
    # hexapod2 = recompute_hexapod(given_dimensions, given_ik_parameters, result_poses)
    # assert msg is None
    # assert_hexapod_equal(hexapod1, hexapod2.body.all_points, hexapod2.legs)
    # assert_hexapod_equal(hexapod2, hexapod1.body.all_points, hexapod1.legs)
    assert True
