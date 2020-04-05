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

names = ['right-middle', 'right-front', 'left-front', 'left-middle', 'left-back', 'right-back']
HEXAPOD_POSE = {}

for i, name in enumerate(names):
  HEXAPOD_POSE[i] = {
    'name': name,
    'id': i,
    'coxia': 0,
    'femur': 0,
    'tibia': 0,
  }

pose_tilted = {
  0: {"coxia": 0, "femur": 5, "tibia": -1, "name": "right-middle", "id": 0},
  1: {"coxia": -18, "femur": 10, "tibia": -2, "name": "right-front", "id": 1},
  2: {"coxia": 28, "femur": 44, "tibia": -43, "name": "left-front", "id": 2},
  3: {"coxia": 0, "femur": 54, "tibia": -43, "name": "left-middle", "id": 3},
  4: {"coxia": -18, "femur": 45, "tibia": -41, "name": "left-back", "id": 4},
  5: {"coxia": 28, "femur": 10, "tibia": 1, "name": "right-back", "id": 5}
}

pose_some_feet_lifted_up  = {
  0: {"coxia": 0, "femur": 5, "tibia": -1, "name": "right-middle", "id": 0},
  1: {"coxia": -18, "femur": 40, "tibia": -30, "name": "right-front", "id": 1},
  2: {"coxia": 28, "femur": 44, "tibia": -43, "name": "left-front", "id": 2},
  3: {"coxia": 0, "femur": 80, "tibia": -43, "name": "left-middle", "id": 3},
  4: {"coxia": -18, "femur": 45, "tibia": -41, "name": "left-back", "id": 4},
  5: {"coxia": 28, "femur": 40, "tibia": 1, "name": "right-back", "id": 5}
}

pose_twisted_lifted_feet = {
  0: {"coxia": 0, "femur": 5, "tibia": -1, "name": "right-middle", "id": 0},
  1: {"coxia": 45, "femur": 40, "tibia": -30, "name": "right-front", "id": 1},
  2: {"coxia": 28, "femur": 44, "tibia": -43, "name": "left-front", "id": 2},
  3: {"coxia": 45, "femur": 80, "tibia": -43, "name": "left-middle", "id": 3},
  4: {"coxia": -18, "femur": 45, "tibia": -41, "name": "left-back", "id": 4},
  5: {"coxia": 45, "femur": 40, "tibia": 1, "name": "right-back", "id": 5}
}

pose_twisted_ground = {
  0: {"coxia": -45, "femur": 5, "tibia": -1, "name": "right-middle", "id": 0},
  1: {"coxia": -18, "femur": 40, "tibia": -30, "name": "right-front", "id": 1},
  2: {"coxia": -45, "femur": 44, "tibia": -43, "name": "left-front", "id": 2},
  3: {"coxia": 0, "femur": 80, "tibia": -43, "name": "left-middle", "id": 3},
  4: {"coxia": -45, "femur": 45, "tibia": -41, "name": "left-back", "id": 4},
  5: {"coxia": 28, "femur": 40, "tibia": 1, "name": "right-back", "id": 5}
}

PREDEFINED_POSES = {
  'NONE': None,
  'neutral': HEXAPOD_POSE,
  'pose-tilted': pose_tilted,
  'pose-lifted-up': pose_some_feet_lifted_up,
  'pose-twist-lifted':pose_twisted_lifted_feet,
  'pose-twist-ground':  pose_twisted_ground,
}