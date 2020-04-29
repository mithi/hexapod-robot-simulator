import numpy as np


def assert_poses_equal(result_poses, correct_poses, description):
    for k, v in result_poses.items():
        msg = f"Unequal Poses\n{correct_poses[k]}\n{v}\n(case: {description})"
        assert correct_poses[k]["name"] == v["name"]
        assert correct_poses[k]["id"] == v["id"]
        assert np.isclose(correct_poses[k]["coxia"], v["coxia"]), msg
        assert np.isclose(correct_poses[k]["femur"], v["femur"]), msg
        assert np.isclose(correct_poses[k]["tibia"], v["tibia"]), msg


def assert_hexapod_points_equal(
    hexapod, correct_body_points, correct_leg_points, description
):
    def msg(a, b):
        return f"Unequal Vectors\nexpected: {a}\n....found: {b}\n(case: {description})"

    for point_a, point_b in zip(correct_body_points, hexapod.body.all_points):
        assert point_a.__eq__(point_b, percent_tol=0.0075), msg(point_a, point_b)

    for leg_set, leg in zip(correct_leg_points, hexapod.legs):
        for point_a, point_b in zip(leg_set, leg.all_points):
            assert point_a.__eq__(point_b, percent_tol=0.0075), msg(point_a, point_b)


def assert_two_hexapods_equal(hexapod1, hexapod2, description):
    def msg(a, b):
        return f"Unequal Vectors\n1: {a}\n2:{b}\n(case: {description})"

    for point_a, point_b in zip(hexapod1.body.all_points, hexapod2.body.all_points):
        assert point_a.__eq__(point_b, percent_tol=0.0075), msg(point_a, point_b)

    for leg_a, leg_b in zip(hexapod1.legs, hexapod2.legs):
        for point_a, point_b in zip(leg_a.all_points, leg_b.all_points):
            assert point_a.__eq__(point_b, percent_tol=0.0075), msg(point_a, point_b)
