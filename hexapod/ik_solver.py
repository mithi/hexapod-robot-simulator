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
  angle_opposite_of_last_side,
  rotz
)

def is_counter_clockwise(a, b, n):
  return dot(a, cross(b, n)) > 0

def sanity_leg_lengths_check(hexapod, leg_name, points):
  coxia = length(vector_from_to(points[0], points[1]))
  femur = length(vector_from_to(points[1], points[2]))
  tibia = length(vector_from_to(points[2], points[3]))

  assert np.isclose(hexapod.coxia, coxia, atol=1), f'wrong coxia vector length. {leg_name} coxia:{coxia}'
  assert np.isclose(hexapod.femur, femur, atol=1), f'wrong femur vector length. {leg_name} femur:{femur}'
  assert np.isclose(hexapod.tibia, tibia, atol=1), f'wrong tibia vector length. {leg_name} tibia:{tibia}'

def print_points(points):
  print(f'p0: {points[0]}')
  print(f'p1: {points[1]}')
  print(f'p2: {points[2]}')
  print(f'p3: {points[3]}')

def find_twist_frame(hexapod, unit_coxia_vector):
  twist = angle_between(unit_coxia_vector, hexapod.x_axis)
  is_ccw = is_counter_clockwise(unit_coxia_vector, hexapod.x_axis, hexapod.z_axis)
  if is_ccw:
    twist_frame = rotz(-twist)
  else:
    twist_frame = rotz(twist)
  return twist_frame

def update_hexapod_points(hexapod, leg_id, points):
  hexapod.legs[leg_id].p0 = points[0]
  hexapod.legs[leg_id].p1 = points[1]
  hexapod.legs[leg_id].p2 = points[2]
  hexapod.legs[leg_id].p3 = points[3]

def body_contact_shoved_on_ground(hexapod):
  for i in range(hexapod.LEG_COUNT):
    body_contact = hexapod.body.vertices[i]
    foot_tip = hexapod.legs[i].foot_tip()
    if body_contact.z < foot_tip.z:
      return True
  return False

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
  poses = deepcopy(HEXAPOD_POSE)

  tx = end_x * hexapod.mid
  ty = end_y * hexapod.side
  tz = end_z * hexapod.tibia

  hexapod.detach_body_rotate_and_translate(rot_x, rot_y, rot_z, tx, ty, tz)
  detached_hexapod = deepcopy(hexapod)

  if body_contact_shoved_on_ground(hexapod):
    return detached_hexapod, None, 'Impossible rotation at given height: body contact shoved on ground'

  for i in range(hexapod.LEG_COUNT):
    leg_name = hexapod.legs[i].name
    body_contact = hexapod.body.vertices[i]
    foot_tip = hexapod.legs[i].foot_tip()
    body_to_foot_vector = vector_from_to(body_contact, foot_tip)
    unit_coxia_vector = project_vector_onto_plane(body_to_foot_vector, hexapod.z_axis)
    coxia_vector = scalar_multiply(unit_coxia_vector, hexapod.coxia)
    coxia_point = add_vectors(body_contact, coxia_vector)

    if coxia_point.z < foot_tip.z:
      return detached_hexapod, None, 'Impossible rotation at given height: coxia joint shoved on ground'

    dd = angle_between(unit_coxia_vector, body_to_foot_vector)
    e = length(body_to_foot_vector)

    p0 = Point(0, 0, 0)
    p1 = Point(hexapod.coxia, 0, 0)
    p3 = Point(e * np.cos(np.radians(dd)), 0, -e * np.sin(np.radians(dd)))

    coxia_to_foot_vector2d = vector_from_to(p1, p3)
    d = length(coxia_to_foot_vector2d)
    aa = angle_opposite_of_last_side(d, hexapod.femur, hexapod.tibia)
    ee = angle_between(coxia_to_foot_vector2d, x_axis)

    CAN_REACH_TARGET_GROUND_POINT = is_triangle(hexapod.tibia, hexapod.femur, d)

    if CAN_REACH_TARGET_GROUND_POINT:

      if p3.z > 0:
        beta = aa + ee
      else:
        beta = aa - ee

      height = -p3.z
      x_ = hexapod.femur * np.cos(np.radians(beta))
      z_ = hexapod.femur * np.sin(np.radians(beta))
      x_ = p1.x + x_
      if height > hexapod.tibia:
        z_ =  -z_
      if beta < 0 and z_ > 0:
        z_ = -z_

      p2 = Point(x_, 0, z_)

      if p2.z < p3.z:
        return detached_hexapod, None, f'{leg_name} leg cant go through ground.'
    else:
      if d + hexapod.tibia < hexapod.femur:
        return detached_hexapod, None, f"Can't reach target ground point. {leg_name} leg's Femur length is too long."
      if d + hexapod.femur < hexapod.tibia:
        return detached_hexapod, None, f"Can't reach target ground point. {leg_name} leg's Tibia length is too long."

      # Then hexapod.femur + hexapod.tibia < d:
      # This means leg's are too short, compute tibia end points in this case
      femur_tibia_direction = get_unit_vector(coxia_to_foot_vector2d)
      femur_vector = scalar_multiply(femur_tibia_direction, hexapod.femur)
      p2 = add_vectors(p1, femur_vector)
      tibia_vector = scalar_multiply(femur_tibia_direction, hexapod.tibia)
      p3 = add_vectors(p2, tibia_vector)

    points = [p0, p1, p2, p3]
    #print_points(points)

    # Find frame used to twist the leg frame wrt to hexapod's body contact point's x axis
    twist_frame = find_twist_frame(hexapod, unit_coxia_vector)

    # Convert points from local leg coordinate frame to world coordinate frame
    for point in points:
      point.update_point_wrt(twist_frame)
      assert hexapod.body_rotation_frame is not None
      point.update_point_wrt(hexapod.body_rotation_frame)
      point.move_xyz(body_contact.x, body_contact.y, body_contact.z)

    # Check if the leg length's are what we expect
    sanity_leg_lengths_check(hexapod, leg_name, points)

    # Update hexapod's points to what we computed
    update_hexapod_points(hexapod, i, points)

  #print(f'poses: {poses}')
  return hexapod, poses, None
