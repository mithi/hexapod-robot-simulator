import numpy as np
from .feetcalculations import get_feet_on_ground
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
  def __init__(self, a, b, c, alpha=0, beta=0, gamma=0, new_x_axis=0, new_origin=Point(0, 0, 0), name=None):
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
    self.p1 = p1.get_point_wrt(new_frame)
    self.p2 = p2.get_point_wrt(new_frame)
    self.p3 = p3.get_point_wrt(new_frame)

    self.p1.name = 'body_contact'
    self.p1.name = 'coxia'
    self.p2.name = 'femur'
    self.p3.name = 'tibia'

  def change_pose(self, alpha=None, beta=None, gamma=None):
    alpha = alpha or self._alpha
    beta = beta or self._beta
    gamma = gamma or self._gamma
    self.save_new_pose(alpha, beta, gamma)

  def toe(self):
    return self.p3

  def z_wrt_body_contact(self):
    #
    #              /*
    #             //\\        
    #            //  \\        
    #           //    \\        
    #          //      \\        
    # *=======* ---->   \\ ---------       
    #                    \\       |
    #                     \\      floor height
    #                      \\     |
    #                       \\ -----
    #
    # |--a--|---b----|
    # *=====*=========* 
    #               | \\
    #               |  \\
    #               |   \\
    #      floor height  \\
    #               |     \\
    #               -      *----------------
    return -self.p3.z

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
  def __init__(self, a=0, b=0, c=0, f=0, m=0, s=0):
    self.linkage_measurements = [a, b, c]
    self.body_measurements = [f, m, s]
    self.body = Hexagon(f, m, s)
    self.store_neutral_legs(a, b, c)

  def store_neutral_legs(self, a, b, c):
    self.legs = []
    for point, theta, name in zip(self.body.vertices, Hexagon.NEW_X_AXES, Hexagon.VERTEX_NAMES):
      linkage = Linkage(a, b, c, new_x_axis=theta, new_origin=point, name=name)
      self.legs.append(linkage)

  def feet_on_ground(self):
    return get_feet_on_ground(self.legs)








