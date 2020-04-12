from hexapod.models import VirtualHexapod
from hexapod.ik_solver.ik_solver import inverse_kinematics_update
import numpy as np
from tests.ik_cases.case1 import given_dimensions, given_ik_parameters, correct_poses


def assert_poses_equal(result_poses, correct_poses):
    for k, v in result_poses.items():
        assert correct_poses[k]["name"] == v["name"]
        assert correct_poses[k]["id"] == v["id"]
        assert np.isclose(correct_poses[k]["coxia"], v["coxia"])
        assert np.isclose(correct_poses[k]["femur"], v["femur"])
        assert np.isclose(correct_poses[k]["tibia"], v["tibia"])


def test_sample_ik():
    hexapod = VirtualHexapod(given_dimensions)
    _, result_poses, msg = inverse_kinematics_update(hexapod, given_ik_parameters)
    assert msg is None
