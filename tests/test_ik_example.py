from hexapod.models import VirtualHexapod
from hexapod.ik_solver import inverse_kinematics_update
import numpy as np

def example_dimensions():
    return {
        "front": 75,
        "side": 150,
        "middle": 125,
        "coxia": 50,
        "femur": 130,
        "tibia": 170,
    }


def example_poses():
    return {
        0: {
            "name": "right-middle",
            "id": 0,
            "coxia": 3.849128962292499,
            "femur": 68.22137487151224,
            "tibia": -33.612289547667885,
        },
        1: {
            "name": "right-front",
            "id": 1,
            "coxia": -15.238968620909759,
            "femur": 84.97509709967663,
            "tibia": -48.556144045861316,
        },
        2: {
            "name": "left-front",
            "id": 2,
            "coxia": 34.759086539818725,
            "femur": 12.54188529413996,
            "tibia": -38.16310045350784,
        },
        3: {
            "name": "left-middle",
            "id": 3,
            "coxia": 39.43137492427002,
            "femur": 7.151051549264324,
            "tibia": -30.453655324475974,
        },
        4: {
            "name": "left-back",
            "id": 4,
            "coxia": 31.649336697508716,
            "femur": 24.832683850986555,
            "tibia": -33.51727069686838,
        },
        5: {
            "name": "right-back",
            "id": 5,
            "coxia": 25.01894554327589,
            "femur": 64.99502764065898,
            "tibia": -20.912070249919225,
        },
    }


def example_ik_parameters():
    return {
        "hip_stance": 13.5,
        "leg_stance": 36,
        "percent_x": -0.45,
        "percent_y": 0.25,
        "percent_z": -0.1,
        "rot_x": 1.5,
        "rot_y": 16.5,
        "rot_z": -9,
    }


def test_ik_example():
    dimensions = example_dimensions()
    ik_parameters = example_ik_parameters()
    correct_poses = example_poses()
    hexapod = VirtualHexapod(dimensions)
    _, result_poses, msg = inverse_kinematics_update(hexapod, ik_parameters)
    assert msg is None
    # assert correct_poses == result_poses # doesn't work with travis
    for k, v in result_poses.items():
        assert correct_poses[k]['name'] == v['name']
        assert correct_poses[k]['id'] == v['id']
        assert np.isclose(correct_poses[k]['coxia'], v['coxia'])
        assert np.isclose(correct_poses[k]['femur'], v['femur'])
        assert np.isclose(correct_poses[k]['tibia'], v['tibia'])
