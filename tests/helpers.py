import numpy as np


def assert_poses_equal(result_poses, correct_poses):
    for k, v in result_poses.items():
        assert correct_poses[k]["name"] == v["name"]
        assert correct_poses[k]["id"] == v["id"]
        assert np.isclose(correct_poses[k]["coxia"], v["coxia"])
        assert np.isclose(correct_poses[k]["femur"], v["femur"])
        assert np.isclose(correct_poses[k]["tibia"], v["tibia"])


def assert_hexapod_equal(hexapod, correct_body_points, correct_leg_points):
    for point_a, point_b in zip(hexapod.body.all_points, correct_body_points):
        assert point_a == point_b, f"{point_a} \n {point_b}"

    for leg, leg_set in zip(hexapod.legs, correct_leg_points):
        for point_a, point_b in zip(leg.all_points, leg_set):
            assert point_a == point_b, f"{point_a} \n {point_b}"
