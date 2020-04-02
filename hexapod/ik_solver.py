from copy import deepcopy
from hexapod.const import HEXAPOD_POSE
import numpy as np
from hexapod.models import VirtualHexapod, Linkage
from hexapod.points import (
  Point,
  dot,
  length,
  scale,
  subtract_vectors,
  add_vectors,
  scalar_multiply,
  vector_from_to,
  get_unit_vector,
  frame_to_align_vector_a_to_b,
  is_triangle_or_line,
  project_vector_onto_plane,
  angle_between,
  angle_opposite_of_last_side
)

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

  hexapod.detach_body_rotate_and_translate(rot_x, rot_y, rot_z, tx, ty, tz)
  body_normal = hexapod.z_axis
  poses = deepcopy(HEXAPOD_POSE)

  for i in range(hexapod.LEG_COUNT):
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
    p1 = add_vectors(p0, coxia_vector2d)
    p3 = body_to_foot_vector2d
    coxia_to_foot_vector2d = vector_from_to(p1, p3)

    a = hexapod.tibia
    b = hexapod.femur
    c = hexapod.coxia
    d = length(vector_from_to(p1, p3))
    e = length(body_to_foot_vector2d)

    aa = angle_opposite_of_last_side(d, b, a)
    bb = angle_opposite_of_last_side(a, d, b)
    dd = angle_opposite_of_last_side(a, b, d)
    ee = angle_between(coxia_vector2d, coxia_to_foot_vector2d)

    alpha_wrt_world = angle_between(coxia_vector, x_axis)
    alpha = alpha_wrt_world - hexapod.body.COXIA_AXES[i]

    CANT_REACH_FOOT_TIP = False
    if is_triangle_or_line(a, b, d):
      beta = -(180 - aa - ee)
      gamma = dd - 90
    else:
      print("Can't reach foot tip")
      CANT_REACH_FOOT_TIP = True
      beta = 0
      gamma = 90

    poses[i]['coxia'] = alpha
    poses[i]['femur'] = beta
    poses[i]['tibia'] = gamma

    if CANT_REACH_FOOT_TIP:
      p2 = deepcopy(p0)
      p3 = deepcopy(p0)
      p2.move_xyz(hexapod.femur, 0, 0)
      p3.move_xyz(hexapod.femur + hexapod.tibia, 0, 0)
    else:
      height = -p3.z
      x_ = b * np.cos(np.radians(beta))
      z_ = b * np.sin(np.radians(beta))
      x_ = p1.x + x_
      if height > a:
        z_ =  -z_ #case 1

      p2 = Point(x_, 0, z_)

    frame = frame_to_align_vector_a_to_b(x_axis, unit_coxia_vector)
    p0.update_point_wrt(frame)
    p1.update_point_wrt(frame)
    p2.update_point_wrt(frame)
    p3.update_point_wrt(frame)
    p0.move_xyz(body_contact.x, body_contact.y, body_contact.z)
    p1.move_xyz(body_contact.x, body_contact.y, body_contact.z)
    p2.move_xyz(body_contact.x, body_contact.y, body_contact.z)
    p3.move_xyz(body_contact.x, body_contact.y, body_contact.z)

    hexapod.legs[i].p0 = p0
    hexapod.legs[i].p1 = p1
    hexapod.legs[i].p2 = p2
    hexapod.legs[i].p3 = p3

  return hexapod, poses
