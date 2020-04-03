from copy import deepcopy
from hexapod.const import HEXAPOD_POSE
import numpy as np
from hexapod.models import VirtualHexapod, Linkage
from hexapod.points import (
  Point,
  cross,
  dot,
  length,
  scale,
  subtract_vectors,
  add_vectors,
  scalar_multiply,
  vector_from_to,
  get_unit_vector,
  frame_to_align_vector_a_to_b,
  is_triangle,
  project_vector_onto_plane,
  angle_between,
  angle_opposite_of_last_side
)

def is_counter_clockwise(a, b, n):
  return dot(a, cross(b, n)) > 0


# CASE 1      <..........x-axis......
#          -         |....c.....|
#         .        /(p1)---- (p0) ....
#        b       /  /       /     .
#       .      /   /      /      .
#      .     /    / d   /       .
#     -   (p2)   /    /        e
#     .     |   /   /         .
#     a     |  /  /          .
#     .     | / /           .
#     _      (p3) ................
#
#
# CASE 2    <......... x-axis .......|
#                      (p2)
#                     / \
#                    /   \
#                   /     \
#                  /       \(p1)-------(p0)
#                 /       /
#                /      /
#               /     /
#              /    /
#             /   /
#            /  /
#            (p3)
#

def inverse_kinematics_update(
  hexapod,
  rot_x,
  rot_y,
  rot_z,
  end_x,
  end_y,
  end_z,
):
  x_axis = Point(1, 0, 0)
  tx = end_x * hexapod.mid
  ty = end_y * hexapod.side
  tz = end_z * hexapod.tibia

  starting_hexapod = deepcopy(hexapod)
  hexapod.detach_body_rotate_and_translate(rot_x, rot_y, rot_z, tx, ty, tz)
  body_normal = hexapod.z_axis
  for i in range(hexapod.LEG_COUNT):
    body_contact = hexapod.body.vertices[i]
    foot_tip = hexapod.legs[i].foot_tip()
    if body_contact.z < foot_tip.z:
      return starting_hexapod, None, 'impossible position'


  print('possible position')
  poses = deepcopy(HEXAPOD_POSE)

  for i in range(hexapod.LEG_COUNT):
    leg_name = hexapod.legs[i].name
    body_contact = hexapod.body.vertices[i]
    foot_tip = hexapod.legs[i].foot_tip()
    body_to_foot_vector = vector_from_to(body_contact, foot_tip)

    #ground_contact = deepcopy(foot_tip)
    unit_coxia_vector = project_vector_onto_plane(body_to_foot_vector, body_normal)
    coxia_vector = scalar_multiply(unit_coxia_vector, hexapod.coxia)

    frame_to_2d = frame_to_align_vector_a_to_b(unit_coxia_vector, x_axis)
    body_to_foot_vector2d = deepcopy(body_to_foot_vector)
    body_to_foot_vector2d.update_point_wrt(frame_to_2d)
    coxia_vector2d = deepcopy(coxia_vector)
    coxia_vector2d.update_point_wrt(frame_to_2d)

    p0 = Point(0, 0, 0)
    p1 = Point(hexapod.coxia, 0.0, 0.0)
    p3 = body_to_foot_vector2d
    p3.y = 0
    coxia_to_foot_vector2d = vector_from_to(p1, p3)

    a = hexapod.tibia
    b = hexapod.femur
    c = hexapod.coxia
    d = length(vector_from_to(p1, p3))
    e = length(body_to_foot_vector2d)

    aa = angle_opposite_of_last_side(d, b, a)
    bb = angle_opposite_of_last_side(a, d, b)
    dd = angle_opposite_of_last_side(a, b, d)

    alpha_wrt_world = angle_between(coxia_vector, x_axis)
    is_ccw = is_counter_clockwise(x_axis, coxia_vector, body_normal)
    alpha = None
    if is_ccw:
      alpha = alpha_wrt_world - hexapod.body.COXIA_AXES[i]
    else:
      alpha = hexapod.body.COXIA_AXES[i] - alpha_wrt_world

    beta = None
    gamma = None
    CANT_REACH_FOOT_TIP = False
    IS_NEUTRAL_POSTION = False
    LEGS_TOO_SHORT = False
    TIBIA_TOO_LONG = False
    FEMUR_TOO_LONG = False

    if np.isclose((c + b)**2 + a**2, d**2):
      print('Neutral position.')
      beta = 0
      gamma = 0
      IS_NEUTRAL_POSTION = True
    if is_triangle(a, b, d):
      print(f'No problems. {leg_name} femur:{b} | tibia:{a} | coxia-to-foot:{d}')
      # This might be wrong, we need to check direction!
      ee = angle_between(coxia_to_foot_vector2d, x_axis)
      beta = aa - ee
      gamma = dd - 90
    else:
      CANT_REACH_FOOT_TIP = True
      print(f"Can't reach foot tip. {leg_name}")
      if a + b < d:
        print("> Legs too short.")
        LEGS_TOO_SHORT = True
        beta = angle_between(coxia_to_foot_vector2d, x_axis)
        CANT_REACH_FOOT_TIP = True
        gamma = 90
      elif d + b < a:
        TIBIA_TOO_LONG = True
        print("> Tibia too long.")

        beta = 90
        p2 = Point(p1.x, 0, b)
        h = -p3.z
        w = np.sqrt(a ** 2 - (b + h)**2)
        p3 = Point(a + w, 0, p3.z)
        tibia_vector = vector_from_to(p2, p3)
        gamma = angle_between(tibia_vector, x_axis)
      else:
        FEMUR_TOO_LONG = True
        alpha = 0
        p2 = Point(c + b, 0, 0)
        h = -p3.z
        w = np.sqrt(a**2 + h**2)
        p3 = Point(b + w, 0, h)
        print("> Femur too long.")

        tibia_vector = vector_from_to(p2, p3)
        gamma = angle_between(tibia_vector, x_axis)

    poses[i]['coxia'] = alpha
    poses[i]['femur'] = beta
    poses[i]['tibia'] = gamma
    if IS_NEUTRAL_POSTION:
      p2 = Point(hexapod.coxia + hexapod.femur, 0, 0)
    elif not CANT_REACH_FOOT_TIP:
      print(f'beta: {beta}')
      height = -p3.z
      x_ = b * np.cos(np.radians(beta))
      z_ = b * np.sin(np.radians(beta))
      x_ = p1.x + x_
      if height > a:
        z_ =  -z_
      if beta < 0:
        if z_ > 0:
          z_ = -z_
      p2 = Point(x_, 0, z_)

      if p2.z < p3.z:
        print('Cant go through ground.')
        beta = -np.arcsin(-p3.z/(a + b))
        gamma = 0
        p2.x = p1.x + b * np.cos(beta)
        p2.z = b * np.sin(beta)
        p3.x = p1.x + (a + b) * np.cos(beta)
    else:
      if LEGS_TOO_SHORT:
        femur_tibia_direction = get_unit_vector(coxia_to_foot_vector2d)
        femur_vector = scalar_multiply(femur_tibia_direction, a)
        p2 = add_vectors(p1, femur_vector)
        tibia_vector = scalar_multiply(femur_tibia_direction, b)
        p3 = add_vectors(p2, tibia_vector)

    print(f'p0: {p0}')
    print(f'p1: {p1}')
    print(f'p2: {p2}')
    print(f'p3: {p3}')

    frame = frame_to_align_vector_a_to_b(x_axis, unit_coxia_vector)
    p0.update_point_wrt(frame)
    p1.update_point_wrt(frame)
    p2.update_point_wrt(frame)
    p3.update_point_wrt(frame)
    p0.move_xyz(body_contact.x, body_contact.y, body_contact.z)
    p1.move_xyz(body_contact.x, body_contact.y, body_contact.z)
    p2.move_xyz(body_contact.x, body_contact.y, body_contact.z)
    p3.move_xyz(body_contact.x, body_contact.y, body_contact.z)

    # Sanity Check
    coxia = length(vector_from_to(p0, p1))
    femur = length(vector_from_to(p1, p2))
    tibia = length(vector_from_to(p2, p3))

    assert np.isclose(hexapod.coxia, coxia, atol=1), f'wrong coxia vector length. {leg_name} coxia:{coxia}'
    assert np.isclose(hexapod.femur, femur, atol=1), f'wrong femur vector length. {leg_name} femur:{femur}'
    assert np.isclose(hexapod.tibia, tibia, atol=1), f'wrong tibia vector length. {leg_name} tibia:{tibia}'

    hexapod.legs[i].p0 = p0
    hexapod.legs[i].p1 = p1
    hexapod.legs[i].p2 = p2
    hexapod.legs[i].p3 = p3

  #print(f'poses: {poses}')
  return hexapod, poses, None
