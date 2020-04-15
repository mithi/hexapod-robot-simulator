from hexapod.models import VirtualHexapod
from tests.kinematics_cases import case1, case2
from tests.helpers import assert_hexapod_equal


def assert_kinematics(case):
    hexapod = VirtualHexapod(case.given_dimensions)
    hexapod.update(case.given_poses)
    assert_hexapod_equal(hexapod, case.correct_body_points, case.correct_leg_points)


def test_sample_kinematics():
    assert_kinematics(case1)
    assert_kinematics(case2)
