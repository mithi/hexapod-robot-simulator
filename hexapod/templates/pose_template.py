# pose = {
#   LEG_ID: {
#     'name': LEG_NAME,
#     'id': LEG_ID
#     'coxia': ALPHA,
#     'femur': BETA,
#     'tibia': GAMMA}
#   }
#   ...
# }

names = [
    "right-middle",
    "right-front",
    "left-front",
    "left-middle",
    "left-back",
    "right-back",
]
HEXAPOD_POSE = {}

for i, name in enumerate(names):
    HEXAPOD_POSE[i] = {
        "name": name,
        "id": i,
        "coxia": 0,
        "femur": 0,
        "tibia": 0,
    }

example_pose = {
    0: {
        "coxia": 16.61,
        "femur": 28.93,
        "tibia": -33.95,
        "name": "right-middle",
        "id": 0,
    },
    1: {
        "coxia": 23.46,
        "femur": 44.83,
        "tibia": -46.41,
        "name": "right-front",
        "id": 1,
    },
    2: {"coxia": 29.53, "femur": 44.86, "tibia": -44.22, "name": "left-front", "id": 2},
    3: {
        "coxia": 28.19,
        "femur": 29.14,
        "tibia": -31.13,
        "name": "left-middle",
        "id": 3,
    },
    4: {"coxia": 29.73, "femur": 15.62, "tibia": -13.95, "name": "left-back", "id": 4},
    5: {"coxia": 20.00, "femur": 15.62, "tibia": -17.44, "name": "right-back", "id": 5},
}

PREDEFINED_POSES = {
    "NONE": None,
    "neutral": HEXAPOD_POSE,
    "example-pose": example_pose,
}
