from hexapod.points import Point

description = "Patterns Random Pose #1"
alpha = 42
beta = 66
gamma = -34.5

# ********************************
# Dimensions
# ********************************

given_dimensions = {
    "front": 76,
    "side": 92,
    "middle": 123,
    "coxia": 58,
    "femur": 177,
    "tibia": 151,
}

# ********************************
# Correct Body Points
# ********************************

correct_body_points = [
    Point(x=+123.00, y=+0.00, z=+0.00, name="right-middle"),
    Point(x=+76.00, y=+92.00, z=+0.00, name="right-front"),
    Point(x=-76.00, y=+92.00, z=+0.00, name="left-front"),
    Point(x=-123.00, y=+0.00, z=+0.00, name="left-middle"),
    Point(x=-76.00, y=-92.00, z=+0.00, name="left-back"),
    Point(x=+76.00, y=-92.00, z=+0.00, name="right-back"),
    Point(x=+0.00, y=+0.00, z=+0.00, name="center-of-gravity"),
    Point(x=+0.00, y=+92.00, z=+0.00, name="head"),
]


# ********************************
# Correct Leg Points
# ********************************

leg0_points = [
    Point(x=+123.00, y=+0.00, z=+0.00, name="right-middle-body-contact"),
    Point(x=+166.10, y=+38.81, z=+0.00, name="right-middle-coxia"),
    Point(x=+219.60, y=+86.98, z=+161.70, name="right-middle-femur"),
    Point(x=+278.24, y=+139.77, z=+32.95, name="right-middle-tibia"),
]

leg1_points = [
    Point(x=+76.00, y=+92.00, z=+0.00, name="right-front-body-contact"),
    Point(x=+79.04, y=+149.92, z=+0.00, name="right-front-coxia"),
    Point(x=+82.80, y=+221.81, z=+161.70, name="right-front-femur"),
    Point(x=+86.93, y=+300.60, z=+32.95, name="right-front-tibia"),
]

leg2_points = [
    Point(x=-76.00, y=+92.00, z=+0.00, name="left-front-body-contact"),
    Point(x=-133.92, y=+95.04, z=+0.00, name="left-front-coxia"),
    Point(x=-205.81, y=+98.80, z=+161.70, name="left-front-femur"),
    Point(x=-284.60, y=+102.93, z=+32.95, name="left-front-tibia"),
]

leg3_points = [
    Point(x=-123.00, y=+0.00, z=+0.00, name="left-middle-body-contact"),
    Point(x=-166.10, y=-38.81, z=+0.00, name="left-middle-coxia"),
    Point(x=-219.60, y=-86.98, z=+161.70, name="left-middle-femur"),
    Point(x=-278.24, y=-139.77, z=+32.95, name="left-middle-tibia"),
]

leg4_points = [
    Point(x=-76.00, y=-92.00, z=+0.00, name="left-back-body-contact"),
    Point(x=-79.04, y=-149.92, z=+0.00, name="left-back-coxia"),
    Point(x=-82.80, y=-221.81, z=+161.70, name="left-back-femur"),
    Point(x=-86.93, y=-300.60, z=+32.95, name="left-back-tibia"),
]

leg5_points = [
    Point(x=+76.00, y=-92.00, z=+0.00, name="right-back-body-contact"),
    Point(x=+133.92, y=-95.04, z=+0.00, name="right-back-coxia"),
    Point(x=+205.81, y=-98.80, z=+161.70, name="right-back-femur"),
    Point(x=+284.60, y=-102.93, z=+32.95, name="right-back-tibia"),
]


correct_leg_points = [
    leg0_points,
    leg1_points,
    leg2_points,
    leg3_points,
    leg4_points,
    leg5_points,
]
