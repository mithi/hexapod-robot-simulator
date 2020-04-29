from hexapod.points import Vector

description = "Kinematics Random Pose #2"

# ********************************
# Dimensions
# ********************************

given_dimensions = {
    "front": 53,
    "side": 112,
    "middle": 124,
    "coxia": 65,
    "femur": 147,
    "tibia": 158,
}

# ********************************
# Poses
# ********************************

given_poses = {
    0: {
        "name": "right-middle",
        "id": 0,
        "coxia": -46.173564612682185,
        "femur": -0.5639873561713742,
        "tibia": -22.853557731606656,
    },
    1: {
        "name": "right-front",
        "id": 1,
        "coxia": -38.57261437211969,
        "femur": -3.2736722565308938,
        "tibia": -24.640160005779748,
    },
    2: {
        "name": "left-front",
        "id": 2,
        "coxia": 2.0526054688295687,
        "femur": 35.09407799312794,
        "tibia": -31.188148885325916,
    },
    3: {
        "name": "left-middle",
        "id": 3,
        "coxia": -16.947073091191385,
        "femur": 46.44561383735447,
        "tibia": -19.412041056143877,
    },
    4: {
        "name": "left-back",
        "id": 4,
        "coxia": -33.39847023693062,
        "femur": 41.05787103974741,
        "tibia": -5.900804146706449,
    },
    5: {
        "name": "right-back",
        "id": 5,
        "coxia": -38.67228081907621,
        "femur": 18.790558327957655,
        "tibia": -30.220554892132796,
    },
}

# ********************************
# Correct Body Vectors
# ********************************

correct_body_points = [
    Vector(x=+112.68, y=+45.33, z=+126.66, name="right-middle"),
    Vector(x=+5.57, y=+122.87, z=+116.68, name="right-front"),
    Vector(x=-90.76, y=+84.12, z=+95.32, name="left-front"),
    Vector(x=-112.68, y=-45.33, z=+76.69, name="left-middle"),
    Vector(x=-5.57, y=-122.87, z=+86.67, name="left-back"),
    Vector(x=+90.76, y=-84.12, z=+108.03, name="right-back"),
    Vector(x=+0.00, y=+0.00, z=+101.67, name="center-of-gravity"),
    Vector(x=-42.60, y=+103.49, z=+106.00, name="head"),
]


# ********************************
# Leg Vectors
# ********************************

leg0_points = [
    Vector(x=+112.68, y=+45.33, z=+126.66, name="right-middle-body-contact"),
    Vector(x=+171.42, y=+18.46, z=+133.92, name="right-middle-coxia"),
    Vector(x=+304.49, y=-42.16, z=+148.91, name="right-middle-femur"),
    Vector(x=+272.70, y=+0.00, z=-0.00, name="right-middle-tibia"),
]


leg1_points = [
    Vector(x=+5.57, y=+122.87, z=+116.68, name="right-front-body-contact"),
    Vector(x=+61.49, y=+153.21, z=+129.97, name="right-front-coxia"),
    Vector(x=+189.21, y=+222.64, z=+151.78, name="right-front-femur"),
    Vector(x=+149.60, y=+203.72, z=-0.00, name="right-front-tibia"),
]

leg2_points = [
    Vector(x=-90.76, y=+84.12, z=+95.32, name="left-front-body-contact"),
    Vector(x=-150.83, y=+107.65, z=+87.44, name="left-front-coxia"),
    Vector(x=-276.55, y=+141.74, z=+155.58, name="left-front-femur"),
    Vector(x=-259.37, y=+163.25, z=+0.00, name="left-front-tibia"),
]

leg3_points = [
    Vector(x=-112.68, y=-45.33, z=+76.69, name="left-middle-body-contact"),
    Vector(x=-176.39, y=-50.56, z=+64.89, name="left-middle-coxia"),
    Vector(x=-293.99, y=-70.60, z=+150.78, name="left-middle-femur"),
    Vector(x=-340.16, y=-60.64, z=-0.00, name="left-middle-tibia"),
]

leg4_points = [
    Vector(x=-5.57, y=-122.87, z=+86.67, name="left-back-body-contact"),
    Vector(x=-58.45, y=-158.23, z=+73.33, name="left-back-coxia"),
    Vector(x=-165.26, y=-229.31, z=+145.09, name="left-back-femur"),
    Vector(x=-217.06, y=-264.36, z=+0.00, name="left-back-tibia"),
]

leg5_points = [
    Vector(x=+90.76, y=-84.12, z=+108.03, name="right-back-body-contact"),
    Vector(x=+121.84, y=-141.20, z=+106.97, name="right-back-coxia"),
    Vector(x=+180.23, y=-268.69, z=+151.07, name="right-back-femur"),
    Vector(x=+191.91, y=-223.89, z=+0.00, name="right-back-tibia"),
]


correct_leg_points = [
    leg0_points,
    leg1_points,
    leg2_points,
    leg3_points,
    leg4_points,
    leg5_points,
]
