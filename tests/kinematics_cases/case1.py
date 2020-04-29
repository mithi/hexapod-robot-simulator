from hexapod.points import Vector

description = "Kinematics Random Pose #1"

# ********************************
# Dimensions
# ********************************

given_dimensions = {
    "front": 75,
    "side": 100,
    "middle": 125,
    "coxia": 50,
    "femur": 130,
    "tibia": 200,
}

# ********************************
# Poses
# ********************************

given_poses = {
    0: {"coxia": -40, "femur": 19, "tibia": 6, "name": "right-middle", "id": 0},
    1: {"coxia": 33, "femur": 85, "tibia": -60, "name": "right-front", "id": 1},
    2: {"coxia": -20, "femur": 90, "tibia": -13, "name": "left-front", "id": 2},
    3: {"coxia": -12, "femur": -25, "tibia": 3, "name": "left-middle", "id": 3},
    4: {"coxia": 0, "femur": 94, "tibia": -70, "name": "left-back", "id": 4},
    5: {"coxia": -5, "femur": 17, "tibia": 2, "name": "right-back", "id": 5},
}


# ********************************
# Correct Body Vectors
# ********************************

correct_body_points = [
    Vector(x=+97.74, y=+69.20, z=+123.97, name="right-middle"),
    Vector(x=-3.68, y=+111.78, z=+103.96, name="right-front"),
    Vector(x=-120.97, y=+28.74, z=+146.94, name="left-front"),
    Vector(x=-97.74, y=-69.20, z=+195.60, name="left-middle"),
    Vector(x=+3.68, y=-111.78, z=+215.60, name="left-back"),
    Vector(x=+120.97, y=-28.74, z=+172.63, name="right-back"),
    Vector(x=+0.00, y=+0.00, z=+159.78, name="center-of-gravity"),
    Vector(x=-62.33, y=+70.26, z=+125.45, name="head"),
]

# ********************************
# Leg Vectors
# ********************************

leg0_points = [
    Vector(x=+97.74, y=+69.20, z=+123.97, name="right-middle-body-contact"),
    Vector(x=+147.72, y=+67.82, z=+124.03, name="right-middle-coxia"),
    Vector(x=+271.07, y=+83.36, z=+162.03, name="right-middle-femur"),
    Vector(x=+353.52, y=-0.00, z=+0.00, name="right-middle-tibia"),
]

leg1_points = [
    Vector(x=-3.68, y=+111.78, z=+103.96, name="right-front-body-contact"),
    Vector(x=-26.03, y=+151.90, z=+84.19, name="right-front-coxia"),
    Vector(x=-29.64, y=+218.89, z=+195.55, name="right-front-femur"),
    Vector(x=-69.47, y=+205.68, z=+0.00, name="right-front-tibia"),
]

leg2_points = [
    Vector(x=-120.97, y=+28.74, z=+146.94, name="left-front-body-contact"),
    Vector(x=-165.74, y=+48.88, z=+137.44, name="left-front-coxia"),
    Vector(x=-164.27, y=+107.00, z=+253.72, name="left-front-femur"),
    Vector(x=-339.26, y=+165.39, z=+176.44, name="left-front-tibia"),
]

leg3_points = [
    Vector(x=-97.74, y=-69.20, z=+195.60, name="left-middle-body-contact"),
    Vector(x=-142.46, y=-88.97, z=+206.04, name="left-middle-coxia"),
    Vector(x=-248.46, y=-160.12, z=+181.51, name="left-middle-femur"),
    Vector(x=-183.54, y=-213.39, z=+0.00, name="left-middle-tibia"),
]

leg4_points = [
    Vector(x=+3.68, y=-111.78, z=+215.60, name="left-back-body-contact"),
    Vector(x=-1.93, y=-156.20, z=+237.87, name="left-back-coxia"),
    Vector(x=+0.55, y=-90.17, z=+349.83, name="left-back-femur"),
    Vector(x=-10.63, y=-244.11, z=+222.63, name="left-back-tibia"),
]

leg5_points = [
    Vector(x=+120.97, y=-28.74, z=+172.63, name="right-back-body-contact"),
    Vector(x=+169.97, y=-37.86, z=+176.57, name="right-back-coxia"),
    Vector(x=+292.24, y=-43.54, z=+220.36, name="right-back-femur"),
    Vector(x=+353.93, y=-139.96, z=+56.35, name="right-back-tibia"),
]

correct_leg_points = [
    leg0_points,
    leg1_points,
    leg2_points,
    leg3_points,
    leg4_points,
    leg5_points,
]
