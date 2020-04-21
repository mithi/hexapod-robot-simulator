from pages.helpers import make_pose
from hexapod.models import VirtualHexapod
from tests.pattern_cases import case1, case2
from tests.helpers import assert_hexapod_points_equal


def test_sample_patterns():
    for case in [case1, case2]:
        for assume_ground_targets in [True, False]:
            poses = make_pose(case.alpha, case.beta, case.gamma)
            hexapod = VirtualHexapod(case.given_dimensions)
            hexapod.update(poses, assume_ground_targets)
            assert_hexapod_points_equal(
                hexapod,
                case.correct_body_points,
                case.correct_leg_points,
                case.description,
            )
