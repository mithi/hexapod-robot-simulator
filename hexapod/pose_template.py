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