description = "IK Random Pose #2"

# ********************************
# Dimensions
# ********************************

given_dimensions = {
    "front": 76,
    "side": 114,
    "middle": 125,
    "coxia": 63,
    "femur": 142,
    "tibia": 171,
}

# ********************************
# IK Parameters
# ********************************

given_ik_parameters = {
    "hip_stance": 10.5,
    "leg_stance": 25.5,
    "percent_x": 0.3,
    "percent_y": 0.05,
    "percent_z": -0.15,
    "rot_x": -1,
    "rot_y": 12.5,
    "rot_z": -8.5,
}

# ********************************
# Poses
# ********************************

correct_poses = {
    0: {
        "name": "right-middle",
        "id": 0,
        "coxia": 13.43107675540267,
        "femur": 77.7924770301091,
        "tibia": -60.647267530564136,
    },
    1: {
        "name": "right-front",
        "id": 1,
        "coxia": 14.431630572348844,
        "femur": 66.33077021197852,
        "tibia": -57.05016213919879,
    },
    2: {
        "name": "left-front",
        "id": 2,
        "coxia": 30.081030614307394,
        "femur": 11.619722581700444,
        "tibia": -1.6253249676582442,
    },
    3: {
        "name": "left-middle",
        "id": 3,
        "coxia": 14.685705676958776,
        "femur": 3.177447435672022,
        "tibia": 4.800985597502901,
    },
    4: {
        "name": "left-back",
        "id": 4,
        "coxia": -0.9115332668632732,
        "femur": 9.309907080761477,
        "tibia": -4.315425166528982,
    },
    5: {
        "name": "right-back",
        "id": 5,
        "coxia": 14.382064236242854,
        "femur": 59.28098836470138,
        "tibia": -49.19348454681213,
    },
}
