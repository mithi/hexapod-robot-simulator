#######################
#
# **********************
# DEFINITIONS
# **********************
# p0: Body contact point
# p1: coxia point / coxia joint (point between coxia limb and femur limb)
# p2: tibia point / tibia joint (point between femur limb and tibia limb)
# p3: foot tip / ground contact
# coxia vector - vector from p0 to p1
# hexapod.coxia - coxia vector length
# femur vector - vector from p1 to p2
# hexapod.femur - femur vector length
# tibia vector - vector from p2 to p3
# hexapod.tibia - tibia vector length
# body_to_foot vector - vector from p0 to p3
# coxia_to_foot vector - vector from p1 to p3
# d: coxia_to_foot_length
# body_to_foot_length
#
# rho
#  -- angle between coxia vector (leg x axis) and body to foot vector
#  -- angle between point p1, p0, and p3. (p0 at center)
# theta
#  --- angle between femur vector and coxia to foot vector
#  --- angle between point p2, p1, and p3. (p1 at center)
# phi
#  --- angle between coxia vector (leg x axis) and coxia to foot vector
#
# beta
#  --- angle between coxia vector (leg x axis) and femur vector
# gamma
#  --- angle between tibia vector and perpendicular vector to femur vector
#  --- positive is counter clockwise
# alpha
#  --- angle between leg coordinate frame and axis defined by line from
#      hexapod's center of gravity to body contact.
#
#
# For CASE 1 and CASE 2:
#   beta = theta - phi
#     beta is positive when phi < theta (case 1)
#     beta is negative when phi > theta (case 2)
# *****************
# Case 1 (beta IS POSITIVE)
# *****************
#
#      ^          (p2)
#      |            *
#  (leg_z_axis)    / |
#      |          /  |
#      |         /   |
#   (p0)    (p1)/    |
#     *------- *-----| ----------------> (leg_x_axis)
#      \       \     |
#        \      \    |
#          \     \   |
#            \    \  |
#              \   \ |
#                \   |
#                  \ * (p3)
#
#
# *****************
# Case 2 (beta is negative)
# *****************
#                           ^
#                           |
#                         (leg_z_axis direction)
# (p0)     (p1)             |
# *------- *----------------|------> (leg_x_axis direction)
# \        |   \
#  \       |    \
#   \      |     \
#    \     |      * (p2)
#     \    |     /
#      \   |    /
#       \  |   /
#        \ |  /
#         \| /
#          *
#
# *****************
# Case 3 (p3 is above p1) then beta = phi + theta
# *****************
#                * (p2)
#               / \
#             /    |
#           /      * (p3)
#         /     /
# *------ *  /
# (p0)   (p1)
########################
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
  is_counter_clockwise,
  project_vector_onto_plane,
  angle_between,
  angle_opposite_of_last_side,
  rotz
)


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
    twist = -twist

  twist_frame = rotz(twist)
  return twist, twist_frame


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

def compute_twist_wrt_to_world(alpha, coxia_axis):
  alpha = (alpha - coxia_axis) % 360
  if alpha > 180:
    alpha = 360 - alpha
  elif alpha < -180:
    alpha =  360 + alpha

  return alpha

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

    # find the coxia vector which is the vector
    # from body contact point to joint between coxia and femur limb
    projection = project_vector_onto_plane(body_to_foot_vector, hexapod.z_axis)
    unit_coxia_vector = get_unit_vector(projection)
    coxia_vector = scalar_multiply(unit_coxia_vector, hexapod.coxia)

    # coxia point / joint is the point connecting the coxia and tibia limbs
    coxia_point = add_vectors(body_contact, coxia_vector)
    if coxia_point.z < foot_tip.z:
      return detached_hexapod, None, 'Impossible rotation at given height: coxia joint shoved on ground'

    # *******************
    # Compute p0, p1 and p3
    # *******************
    # p0 and p1 in the local leg frame is straight forward
    p0 = Point(0, 0, 0)
    p1 = Point(hexapod.coxia, 0, 0)

    # Find p3 aka foot tip (ground contact) with respect to the local leg frame
    rho = angle_between(unit_coxia_vector, body_to_foot_vector)
    body_to_foot_length = length(body_to_foot_vector)
    p3x = body_to_foot_length * np.cos(np.radians(rho))
    p3z = -body_to_foot_length * np.sin(np.radians(rho))
    p3 = Point(p3x, 0, p3z)

    # *******************
    # Compute p2, beta and gamma
    # *******************
    # These values are needed to compute
    # p2 aka tibia joint (point between femur limb and tibia limb)

    coxia_to_foot_vector2d = vector_from_to(p1, p3)
    d = length(coxia_to_foot_vector2d)
    theta = angle_opposite_of_last_side(d, hexapod.femur, hexapod.tibia)
    phi = angle_between(coxia_to_foot_vector2d, x_axis)

    # If we can form this triangle this means we can reach the target ground contact point
    CAN_REACH_TARGET_GROUND_POINT = is_triangle(hexapod.tibia, hexapod.femur, d)

    if CAN_REACH_TARGET_GROUND_POINT:
      beta = theta - phi
      if p3.z > 0:
        beta = theta + phi

      z_ = hexapod.femur * np.sin(np.radians(beta))
      x_ = p1.x + hexapod.femur * np.cos(np.radians(beta))

      p2 = Point(x_, 0, z_)
      femur_vector = vector_from_to(p1, p2)
      tibia_vector = vector_from_to(p2, p3)
      gamma = 90 - angle_between(femur_vector, tibia_vector)

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

      # find beta and gamma
      gamma = 0.0
      leg_x_axis = Point(1, 0, 0)
      beta = angle_between(leg_x_axis, femur_vector)
      if femur_vector.z < 0:
        beta = -beta

    # *******************
    # Update hexapod points and get pose angles
    # *******************
    points = [p0, p1, p2, p3]
    #print_points(points)

    # Find frame used to twist the leg frame wrt to hexapod's body contact point's x axis
    alpha, twist_frame = find_twist_frame(hexapod, unit_coxia_vector)

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

    alpha = compute_twist_wrt_to_world(alpha, hexapod.body.COXIA_AXES[i])

    poses[i]['coxia'] = alpha
    poses[i]['femur'] = beta
    poses[i]['tibia'] = gamma

  return hexapod, poses, None

# Notes:
# - Limit alpha to range between -90 to 90
# - Also limit beta and gamma to better ranges
# - When all left side or right side is above ground, make this an impossible pose.
# - Make ik solver a class to breakdown the large method
# - Name the updated points of the updated hexapod their correct names, right now they're names is None
# - Check if the pose of the hexapod is stable (IE the center of gravity falls in Hexy's support polygon)