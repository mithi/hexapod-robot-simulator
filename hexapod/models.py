import numpy as np
from .ground_contact_calculator import get_legs_on_ground
from .points import Point, frame_yrotate_xtranslate, frame_zrotate_xytranslate
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
    self.id = id_number
    self.name = name
    self.store_linkage_attributes(a, b, c, new_x_axis, new_origin)
    self.save_new_pose(alpha, beta, gamma)

  def store_linkage_attributes(self, a, b, c, new_x_axis, new_origin):
    self._a = a
    self._b = b
    self._c = c
    self._new_origin = new_origin
    self._new_x_axis = new_x_axis

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
    self.p0 = self._new_origin
    self.p0.name = 'body_contact'

    self.p1 = p1.get_point_wrt(new_frame, name='coxia')
    self.p2 = p2.get_point_wrt(new_frame, name='femur')
    self.p3 = p3.get_point_wrt(new_frame, name='tibia')

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

  def tip_wrt_cog(self):
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
  
  def femur_wrt_cog(self):
    return -self.femur_point().z
  
  def compute_ground_contact(self):
    if self.tip_wrt_cog() <= 0:
      if self.femur_wrt_cog() <= 0:
        return self.coxia_point()
      else:
        return self.femur_point()

    if self.tip_wrt_cog() >= self.femur_wrt_cog():
      return self.foot_tip()
    else:
      return self.femur_point()
  
  def ground_contact(self):
    return self.ground_contact_point


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

    self.cog = Point(0, 0, 0)
    self.head = Point(0, s, 0)
    self.vertices = [
      Point(m, 0, 0),
      Point(f, s, 0),
      Point(-f, s, 0),
      Point(-m, 0, 0),
      Point(-f, -s, 0),
      Point(f, -s, 0),
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
    return self

  def store_neutral_legs(self, a, b, c):
    self.legs = []
    vertices, axes, names = self.body.vertices, Hexagon.NEW_X_AXES, Hexagon.VERTEX_NAMES
    for i, point, theta, name in zip(range(6), vertices, axes, names):
      linkage = Linkage(a, b, c, new_x_axis=theta, new_origin=point, name=name, id_number=i)
      self.legs.append(linkage)

  def ground_contact_points(self):
    legs = get_legs_on_ground(self.legs)
    ground_contact = [leg.ground_contact() for leg in legs]
    return ground_contact
  
  def update(self, poses):
    # pose = { 
    #   LEG_ID: {
    #     'name': LEG_NAME, 
    #     'id': LEG_ID
    #     'coxia': ALPHA, 
    #     'femur': BETA, 
    #     'tibia': GAMMA}
    #   }
    #   ...
    # }
    for _, pose in poses.items():
      i = pose['id']
      alpha = pose['coxia']
      beta = pose['femur']
      gamma = pose['tibia']
      self.legs[i].change_pose(alpha, beta, gamma)




