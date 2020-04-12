from hexapod.models import VirtualHexapod
from tests.kinematics_cases import case1


def assert_hexapod_equal(hexapod, correct_body_points, correct_leg_points):
    for point_a, point_b in zip(hexapod.body.all_points, correct_body_points):
        assert point_a == point_b, f"{point_a} != {point_b}"

    for leg, leg_set in zip(hexapod.legs, correct_leg_points):
        for point_a, point_b in zip(leg.all_points, leg_set):
            assert point_a == point_b, f"{point_a} != {point_b}"


def test_sample_kinematics():
    hexapod = VirtualHexapod(case1.given_dimensions)
    hexapod.update(case1.given_poses)
    assert_hexapod_equal(hexapod, case1.correct_body_points, case1.correct_leg_points)
