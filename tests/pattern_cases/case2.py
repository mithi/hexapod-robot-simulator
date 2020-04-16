from hexapod.points import Point

description = "Patterns Random Pose #2"
alpha = -28.5
beta = 72
gamma = -54

# ********************************
# Dimensions
# ********************************

given_dimensions = {
    "front": 65,
    "side": 101,
    "middle": 122,
    "coxia": 83,
    "femur": 108,
    "tibia": 177,
}

# ********************************
# Correct Body Points
# ********************************

correct_body_points = [
    Point(x=+116.86, y=+35.03, z=+65.62, name="right-middle"),
    Point(x=+33.27, y=+115.41, z=+65.62, name="right-front"),
    Point(x=-91.26, y=+78.09, z=+65.62, name="left-front"),
    Point(x=-116.86, y=-35.03, z=+65.62, name="left-middle"),
    Point(x=-33.27, y=-115.41, z=+65.62, name="left-back"),
    Point(x=+91.26, y=-78.09, z=+65.62, name="right-back"),
    Point(x=+0.00, y=+0.00, z=+65.62, name="center of gravity"),
    Point(x=-29.00, y=+96.75, z=+65.62, name="head"),
]


# ********************************
# Correct Leg Points
# ********************************
leg0_points = [
    Point(x=+116.86, y=+35.03, z=+65.62, name="right-middle-body-contact"),
    Point(x=+198.11, y=+18.03, z=+65.62, name="right-middle-coxia"),
    Point(x=+230.77, y=+11.20, z=+168.34, name="right-middle-femur"),
    Point(x=+284.31, y=+0.00, z=+0.00, name="right-middle-tibia"),
]

leg1_points = [
    Point(x=+33.27, y=+115.41, z=+65.62, name="right-front-body-contact"),
    Point(x=+102.73, y=+160.84, z=+65.62, name="right-front-coxia"),
    Point(x=+130.66, y=+179.11, z=+168.34, name="right-front-femur"),
    Point(x=+176.44, y=+209.04, z=+0.00, name="right-front-tibia"),
]

leg2_points = [
    Point(x=-91.26, y=+78.09, z=+65.62, name="left-front-body-contact"),
    Point(x=-136.69, y=+147.55, z=+65.62, name="left-front-coxia"),
    Point(x=-154.96, y=+175.48, z=+168.34, name="left-front-femur"),
    Point(x=-184.90, y=+221.26, z=+0.00, name="left-front-tibia"),
]

leg3_points = [
    Point(x=-116.86, y=-35.03, z=+65.62, name="left-middle-body-contact"),
    Point(x=-198.11, y=-18.03, z=+65.62, name="left-middle-coxia"),
    Point(x=-230.77, y=-11.20, z=+168.34, name="left-middle-femur"),
    Point(x=-284.31, y=+0.00, z=+0.00, name="left-middle-tibia"),
]

leg4_points = [
    Point(x=-33.27, y=-115.41, z=+65.62, name="left-back-body-contact"),
    Point(x=-102.73, y=-160.84, z=+65.62, name="left-back-coxia"),
    Point(x=-130.66, y=-179.11, z=+168.34, name="left-back-femur"),
    Point(x=-176.44, y=-209.04, z=+0.00, name="left-back-tibia"),
]

leg5_points = [
    Point(x=+91.26, y=-78.09, z=+65.62, name="right-back-body-contact"),
    Point(x=+136.69, y=-147.55, z=+65.62, name="right-back-coxia"),
    Point(x=+154.96, y=-175.48, z=+168.34, name="right-back-femur"),
    Point(x=+184.90, y=-221.26, z=+0.00, name="right-back-tibia"),
]

correct_leg_points = [
    leg0_points,
    leg1_points,
    leg2_points,
    leg3_points,
    leg4_points,
    leg5_points,
]
