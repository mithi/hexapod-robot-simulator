import numpy as np
from .ground_contact_calculator import get_legs_on_ground
from .points import Point, frame_yrotate_xtranslate, frame_zrotate_xytranslate, frame_to_align_vector_a_to_b
from copy import deepcopy
# -------------
# LINKAGE
# -------------
# Neutral position of the linkages (alpha=0, beta=0, gamma=0)
# note that at neutral position:
#  link b and link c are perpendicular to each other
#  link a and link b form a straight line
#  link a coincide with x axis
#
# alpha - the able linkage a makes with x_axis about z axis
# beta - the angle that linkage a makes with linkage b
# gamma - the angle that linkage c make with the line perpendicular to linkage b
#
#
# MEASUREMENTS
#
#  |--- a--------|--b--|
#  |=============|=====| p2 -------
#  p0            p1    |          |
#                      |          |
#                      |          c
#                      |          |
#                      |          |
#                      | p3  ------
#
# p0 - body contact
# p1 - coxia point
# p2 - femur point
# p3 - foot tip
#
#  z axis
#  |
#  |
#  |------- x axis
# origin
#
#
# ANGLES beta and gamma
#                /
#               / beta
#         ---- /* ---------
#        /    //\\        \
#       b    //  \\        \
#      /    //    \\        c
#     /    //beta  \\        \
# *=======* ---->   \\        \
# |---a---|          \\        \
#                     *-----------
#
# |--a--|---b----|
# *=====*=========* -------------
#               | \\            \
#               |  \\            \
#               |   \\            c
#               |    \\            \
#               |gamma\\            \
#               |      *----------------
#
class Linkage:
  POINT_NAMES = ['coxia', 'femur', 'tibia']
  def __init__(self, a, b, c, alpha=0, beta=0, gamma=0, new_x_axis=0, new_origin=Point(0, 0, 0), name=None, id_number=None):
    self.store_linkage_attributes(a, b, c, new_x_axis, new_origin, name, id_number)
    self.save_new_pose(alpha, beta, gamma)

  def store_linkage_attributes(self, a, b, c, new_x_axis, new_origin, name, id_number):
    self._a = a
    self._b = b
    self._c = c
    self._new_origin = new_origin
    self._new_x_axis = new_x_axis
    self.id = id_number
    self.name = name

  def save_new_pose(self, alpha, beta, gamma):
    self._alpha = alpha
    self._beta = beta
    self._gamma = gamma

    # frame_ab is the pose of frame_b wrt frame_a
    frame_01 = frame_yrotate_xtranslate(theta=-self._beta, x=self._a)
    frame_12 = frame_yrotate_xtranslate(theta=90-self._gamma, x=self._b)
    frame_23 = frame_yrotate_xtranslate(theta=0, x=self._c)

    frame_02 = np.matmul(frame_01, frame_12)
    frame_03 = np.matmul(frame_02, frame_23)
    new_frame = frame_zrotate_xytranslate(self._new_x_axis + self._alpha, self._new_origin.x, self._new_origin.y)

    # find points wrt to body contact point
    p0 = Point(0, 0, 0)
    p1 = p0.get_point_wrt(frame_01)
    p2 = p0.get_point_wrt(frame_02)
    p3 = p0.get_point_wrt(frame_03)

    # find points wrt to center of gravity
    self.p0 = deepcopy(self._new_origin)
    self.p0.name += 'body-contact'
    self.p1 = p1.get_point_wrt(new_frame, name=self.name+'-coxia')
    self.p2 = p2.get_point_wrt(new_frame, name=self.name+'-femur')
    self.p3 = p3.get_point_wrt(new_frame, name=self.name+'-tibia')

    self.ground_contact_point = self.compute_ground_contact()

  def change_pose(self, alpha=None, beta=None, gamma=None):
    alpha = alpha or self._alpha
    beta = beta or self._beta
    gamma = gamma or self._gamma
    self.save_new_pose(alpha, beta, gamma)

  def coxia_angle(self):
    return self._alpha

  def coxia_point(self):
    return self.p1

  def femur_point(self):
    return self.p2

  def foot_tip(self):
    return self.p3

  def _tip_wrt_cog(self):
    #
    #          /*
    #         //\\
    #        //  \\
    #       //    \\
    #      //      \\
    # *===* ---->   \\ ---------
    #                \\       |
    #                 \\   tip height (positive)
    #                  \\     |
    #                   \\ -----
    #
    #
    # *===*=======*
    #           | \\
    #           |  \\
    # (positive)|   \\
    #    tip height  \\
    #           |     \\
    #         ------    *----
    #
    #                *=========* -----
    #               //             |
    #              // (negative) tip height
    #             //               |
    #*===*=======*  -------------------
    # Negative only if body contact point
    # is touching the ground
    return -self.foot_tip().z

  def _femur_wrt_cog(self):
    return -self.femur_point().z

  def compute_ground_contact(self):
    if self._tip_wrt_cog() <= 0:
      if self._femur_wrt_cog() <= 0:
        return self.coxia_point()
      else:
        return self.femur_point()

    if self._tip_wrt_cog() >= self._femur_wrt_cog():
      return self.foot_tip()
    else:
      return self.femur_point()

  def ground_contact(self):
    return self.ground_contact_point

  def update_leg_wrt(self, frame, height):
      self.p0.update_point_wrt(frame, height)
      self.p1.update_point_wrt(frame, height)
      self.p2.update_point_wrt(frame, height)
      self.p3.update_point_wrt(frame, height)

# MEASUREMENTS f, s, and m
#
#       |-f-|
#       *---*---*--------
#      /    |    \     |
#     /     |     \    s
#    /      |      \   |
#   *------cog------* ---
#    \      |      /|
#     \     |     / |
#      \    |    /  |
#       *---*---*   |
#           |       |
#           |---m---|
#
#    y axis
#    ^
#    |
#    |
#    ----> x axis
#  cog (origin)
#
#
# Relative x-axis, for each attached linkage
#
#         x2          x1
#          \         /
#           *---*---*
#          /    |    \
#         /     |     \
#        /      |      \
#  x3 --*------cog------*-- x0
#        \      |      /
#         \     |     /
#          \    |    /
#           *---*---*
#          /         \
#         x4         x5
#
class Hexagon:
  VERTEX_NAMES = ['right-middle', 'right-front', 'left-front', 'left-middle', 'left-back', 'right-back']
  NEW_X_AXES = [0, 45, 135, 180, 225, 315]
  def __init__(self, f, m, s):
    self.f = f
    self.m = m
    self.s = s

    self.cog = Point(0, 0, 0, name='center of gravity')
    self.head = Point(0, s, 0, name='head')
    self.vertices = [
      Point(m, 0, 0, name=Hexagon.VERTEX_NAMES[0]),
      Point(f, s, 0, name=Hexagon.VERTEX_NAMES[1]),
      Point(-f, s, 0, name=Hexagon.VERTEX_NAMES[2]),
      Point(-m, 0, 0, name=Hexagon.VERTEX_NAMES[3]),
      Point(-f, -s, 0, name=Hexagon.VERTEX_NAMES[4]),
      Point(f, -s, 0, name=Hexagon.VERTEX_NAMES[5]),
    ]

class VirtualHexapod:
  def __init__(self, measurements=None):
    if measurements is None:
      self.new()
    else:
      f, s, m = measurements['front'], measurements['side'], measurements['middle'],
      h, k, a = measurements['coxia'], measurements['femur'], measurements['tibia']
      self.new(f, m, s, h, k, a)

  def new(self, f=0, m=0, s=0, a=0, b=0, c=0):
    # coxia length, femur length, tibia length
    self.linkage_measurements = [a, b, c]
    # front length, middle length, side length
    self.body_measurements = [f, m, s]

    self.body = Hexagon(f, m, s)
    self.store_neutral_legs(a, b, c)
    self.ground_contacts = [leg.foot_tip() for leg in self.legs]

    # Initialize local coordinate frame
    self.x_axis = Point(1, 0, 0, name='hexapod x axis')
    self.y_axis = Point(0, 1, 0, name='hexapod y axis')
    self.z_axis = Point(0, 0, 1, name='hexapod z axis')
    return self

  def update(self, poses):
    # Check the possibility of hexapod twisting about z axis
    might_twist = self.find_if_might_twist(poses)
    # Remember old ground contacts
    old_ground_contacts = deepcopy(self.ground_contacts)

    # Change each leg's pose
    for _, leg_pose in poses.items():
      i = leg_pose['id']
      alpha = leg_pose['coxia']
      beta = leg_pose['femur']
      gamma = leg_pose['tibia']
      self.legs[i].change_pose(alpha, beta, gamma)

    # Update which legs are on the ground
    # The new 'normal', and height
    legs, self.n_axis, height = get_legs_on_ground(self.legs)
    self.ground_contacts = [leg.ground_contact() for leg in legs]

    # This means that the position is stable
    if self.n_axis is not None:
      # tilt and shift the hexapod based on new normal
      frame = frame_to_align_vector_a_to_b(self.n_axis, Point(0, 0, 1))
      self.update_local_frame(frame)
      self.rotate_and_shift(frame, height)

      # Only twist if we computed earlier that at least three hips twisted
      if might_twist:
        twist_frame = find_twist(old_ground_contacts, self.ground_contacts)
        self.rotate_and_shift(twist_frame, 0)
    else:
      pass
      # IMPORTANT!!:
      # if the position is not stable, what to do?
      # right now it just displays the figure like
      # there's no gravity

  def find_if_might_twist(self, poses):
    # hexapod will only definitely NOT twist
    # if only two of the legs (currently on the ground)
    # has twisted its hips/coxia
    # i.e. only 2 legs with ground contact points have changed alpha angle
    # i.e. we don't care if the legs which are not on the ground twisted its hips
    did_change_count = 0

    for leg_point in self.ground_contacts:

      # gind the leg id of the ground contact point
      right_or_left, front_mid_or_back, _ = leg_point.name.split('-')
      leg_placement =  right_or_left + '-' + front_mid_or_back
      leg_id = self.body.VERTEX_NAMES.index(leg_placement)

      # alpha before new pose
      old_hip_angle = self.legs[leg_id].coxia_angle()

      # new alpha pose
      new_hip_angle = None
      try:
        new_hip_angle = poses[leg_id]['coxia']
      except:
        new_hip_angle = poses[str(leg_id)]['coxia']

      if not np.isclose(old_hip_angle, new_hip_angle or 0):
        did_change_count += 1
        if did_change_count >= 3:
          return True

    return False

  def store_neutral_legs(self, a, b, c):
    self.legs = []
    vertices, axes, names = self.body.vertices, Hexagon.NEW_X_AXES, Hexagon.VERTEX_NAMES
    for i, point, theta, name in zip(range(6), vertices, axes, names):
      linkage = Linkage(a, b, c, new_x_axis=theta, new_origin=point, name=name, id_number=i)
      self.legs.append(linkage)

  def ground_contact_points(self):
    return self.ground_contacts

  def update_local_frame(self, frame):
    self.x_axis.update_point_wrt(frame, 0)
    self.y_axis.update_point_wrt(frame, 0)
    self.z_axis.update_point_wrt(frame, 0)

  def rotate_and_shift(self, frame, height):
    # Update cog and head
    self.body.cog.update_point_wrt(frame, height)
    self.body.head.update_point_wrt(frame, height)

    # Update each point in body hexagon
    for vertex in self.body.vertices:
      vertex.update_point_wrt(frame, height)

    # Update each point in each leg
    for leg in self.legs:
      leg.update_leg_wrt(frame, height)

def find_twist(old_ground_contacts, new_ground_contacts):
  # This is the frame used to twist the model about the z axis

  def _make_contact_dict(contact_list):
    contact_dict = {}
    for leg_point in contact_list:
      name = leg_point.name
      contact_dict[name] = leg_point
    return contact_dict

  def _twist(v1, v2):
    # Note: theta is in radians
    # https://www.euclideanspace.com/maths/algebra/vectors/angleBetween/
    theta = np.arctan2(v2.y, v2.x) - np.arctan2(v1.y, v1.x)

    # frame to rotate around z
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    return np.array([
      [cos_theta, -sin_theta, 0, 0],
      [sin_theta, cos_theta, 0, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 1],
    ])

  # Make dictionary mapping contact point name and leg_contact_point
  old_contacts = _make_contact_dict(old_ground_contacts)
  new_contacts = _make_contact_dict(new_ground_contacts)

  # Find at least one point that's the same
  same_point_name = None
  for key in old_contacts.keys():
    if key in new_contacts.keys():
      same_point_name = key
      break

  # We don't know how to rotate if we don't
  # know at least one point that's contacting the ground
  # before and after the movement
  # so we assume that the hexapod didn't move
  if same_point_name == None:
    return np.eye(4)

  old = old_contacts[same_point_name]
  new = new_contacts[same_point_name]

  # Get the projection of these points in the ground
  old_vector = Point(old.x, old.y, 0)
  new_vector = Point(new.x, new.y, 0)

  # Fix: Why is this not working?? 😢
  # wrong_twist_frame = frame_to_align_vector_a_to_b(new_vector, old_vector)

  twist_frame = _twist(new_vector, old_vector)

  # IMPORTANT: We are assuming that because the point
  # is on the ground before and after
  # They should be at the same point after movement
  # I can't think of a case that contradicts this as of this moment
  return twist_frame