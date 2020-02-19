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

  def tilt_and_shift(self, frame, height):
    # Update cog and head
    self.body.cog.update_point_wrt(frame, height)
    self.body.head.update_point_wrt(frame, height)

    # Update each point in body hexagon
    for vertex in self.body.vertices:
      vertex.update_point_wrt(frame, height)

    # Update each point in each leg
    for leg in self.legs:
      leg.update_leg_wrt(frame, height)

  def update(self, poses):

    # Change each leg's pose
    for _, pose in poses.items():
      i = pose['id']
      alpha = pose['coxia']
      beta = pose['femur']
      gamma = pose['tibia']
      self.legs[i].change_pose(alpha, beta, gamma)

    # Update which legs are on the ground
    # The new 'normal', and height 
    legs, self.n_axis, height = get_legs_on_ground(self.legs)
    self.ground_contacts = [leg.ground_contact() for leg in legs]

    if self.n_axis is not None:
      # tilt and shift the hexapod based on new normal
      frame = frame_to_align_vector_a_to_b(self.n_axis, Point(0, 0, 1))
      self.update_local_frame(frame)
      self.tilt_and_shift(frame, height)

    # The position is not stable, what to do?
    # Right now it just displays the figure like 
    # There's no gravity