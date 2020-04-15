from hexapod.points import is_counter_clockwise, angle_between, rotz


def update_hexapod_points(hexapod, leg_id, points):
    points[0].name = hexapod.legs[leg_id].p0.name
    points[1].name = hexapod.legs[leg_id].p1.name
    points[2].name = hexapod.legs[leg_id].p2.name
    points[3].name = hexapod.legs[leg_id].p3.name

    hexapod.legs[leg_id].p0 = points[0]
    hexapod.legs[leg_id].p1 = points[1]
    hexapod.legs[leg_id].p2 = points[2]
    hexapod.legs[leg_id].p3 = points[3]


def find_twist_frame(hexapod, unit_coxia_vector):
    twist = angle_between(unit_coxia_vector, hexapod.x_axis)
    is_ccw = is_counter_clockwise(unit_coxia_vector, hexapod.x_axis, hexapod.z_axis)
    if is_ccw:
        twist = -twist

    twist_frame = rotz(twist)
    return twist, twist_frame


def compute_twist_wrt_to_world(alpha, coxia_axis):
    alpha = (alpha - coxia_axis) % 360
    if alpha > 180:
        alpha = alpha - 360
    elif alpha < -180:
        alpha = 360 + alpha

    return alpha
