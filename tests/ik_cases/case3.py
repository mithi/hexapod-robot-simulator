description = "IK Pose where x, y translation, rot y and z are close to extreme"

# ********************************
# Dimensions
# ********************************

given_dimensions = {
    "front": 73,
    "side": 100,
    "middle": 130,
    "coxia": 75,
    "femur": 129,
    "tibia": 154,
}

# ********************************
# IK Parameters
# ********************************

given_ik_parameters = {
    "hip_stance": 10.5,
    "leg_stance": 30,
    "percent_x": 0.7,
    "percent_y": -0.4,
    "percent_z": 0.2,
    "rot_x": 1.5,
    "rot_y": -16,
    "rot_z": -14.5,
}

# ********************************
# Poses
# ********************************

correct_poses = {
    0: {
        "name": "right-middle",
        "id": 0,
        "coxia": 55.56073526445866,
        "femur": -24.206649398630788,
        "tibia": -8.608209643253758,
    },
    1: {
        "name": "right-front",
        "id": 1,
        "coxia": 51.072817817160114,
        "femur": -5.7010123660724545,
        "tibia": -7.5181271777452565,
    },
    2: {
        "name": "left-front",
        "id": 2,
        "coxia": 33.84438606600443,
        "femur": 30.76781937225195,
        "tibia": 16.92773639721497,
    },
    3: {
        "name": "left-middle",
        "id": 3,
        "coxia": 13.117976527545807,
        "femur": 48.11622597324919,
        "tibia": -0.4754969993002618,
    },
    4: {
        "name": "left-back",
        "id": 4,
        "coxia": -8.445805980297905,
        "femur": 53.09741126074167,
        "tibia": -21.001329834229722,
    },
    5: {
        "name": "right-back",
        "id": 5,
        "coxia": 26.002763598408308,
        "femur": -17.792174423794933,
        "tibia": -25.026074825755416,
    },
}
