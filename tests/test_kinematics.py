from hexapod.models import VirtualHexapod
from tests.kinematics_cases import case1
from tests.helpers import assert_hexapod_equal


def test_sample_kinematics():
    hexapod = VirtualHexapod(case1.given_dimensions)
    hexapod.update(case1.given_poses)
    assert_hexapod_equal(hexapod, case1.correct_body_points, case1.correct_leg_points)
