import numpy as np
import plotly.graph_objects as go

# rotate about y, translate in x
def frame_yrotate_xtranslate(theta, x):
  theta = np.radians(theta)
  cos_theta = np.cos(theta)
  sin_theta = np.sin(theta)

  return np.array([
    [cos_theta, 0, sin_theta, x],
    [0, 1, 0, 0],
    [-sin_theta, 0, cos_theta, 0],
    [0, 0, 0, 1]
  ])

# rotate about z, translate in x and y
def frame_zrotate_xytranslate(theta, x, y):
  theta = np.radians(theta)
  cos_theta = np.cos(theta)
  sin_theta = np.sin(theta)

  return np.array([
    [cos_theta, -sin_theta, 0, x],
    [sin_theta, cos_theta, 0, y],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
  ])

class Point:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def get_point_wrt(self, reference_frame):
    # given frame_ab which is the pose of frame_b wrt frame_a
    # given a point as defined wrt to frame_b
    # return point defined wrt to frame a
    p = np.array([self.x, self.y, self.z, 1])
    p = np.matmul(reference_frame, p)
    return Point(p[0], p[1], p[2])

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
  def __init__(self, a, b, c, alpha=0, beta=0, gamma=0, new_x_axis=0, new_origin=Point(0, 0, 0)):
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

  def change_pose(self, alpha=None, beta=None, gamma=None):
    if alpha is None:
      alpha = self._alpha
    if beta is None:
      beta = self._beta
    if gamma is None:
      gamma = self._gamma
    self.save_new_pose(alpha, beta, gamma)

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
#        x2         x1
#         \         /
#          *---*---*
#         /    |    \
#        /     |     \
#       /      |      \
#  x3--*------cog------*--x0
#       \      |      /
#        \     |     /
#         \    |    /
#          *---*---*
#         /        \
#        x4        x5
#
class Hexagon:
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

    self.new_x_axes = [
      0, 45, 135, 180, 225, 315
    ]

class VirtualHexapod:
  def __init__(self, a=0, b=0, c=0, f=0, m=0, s=0):
    self.linkage_measurements = [a, b, c]
    self.body_measurements = [f, m, s]
    self.body = Hexagon(f, m, s)
    self.store_neutral_legs(a, b, c)

  def store_neutral_legs(self, a, b, c):
    self.legs = []
    for point, theta in zip(self.body.vertices, self.body.new_x_axes):
      linkage = Linkage(a, b, c, new_x_axis=theta, new_origin=point)
      self.legs.append(linkage)

class HexapodPlot:
  LINE_SIZE = 10
  HEAD_SIZE = 15
  COG_SIZE = 10
  BODY_COLOR = '#8e44ad'
  COG_COLOR = '#e74c3c'
  LEG_COLOR = '#2c3e50'

  def __init__(self, _hexapod):
    self.fig = go.FigureWidget()
    self.hexapod = _hexapod
    self.draw()
    self._configure()

  def _configure(self):
    self.fig.update_layout(
      autosize=False,
      width=700,
      height=700,
      scene={
        'xaxis': { 'range': [-200, 200] },
        'yaxis': { 'range': [-200, 200] },
        'zaxis': { 'range': [-200, 200] },
        'aspectmode': 'manual',
        'aspectratio': go.layout.scene.Aspectratio(x=1, y=1, z=1)
      },
    )
        
  def _draw_lines(self, _name, _points, _size, _color, _is_name_visible=True):
    self.fig.add_trace(go.Scatter3d(
      name=_name,
      x=[point.x for point in _points],
      y=[point.y for point in _points],
      z=[point.z for point in _points],
      line={
        'color': _color,
        'width': _size
      },
      showlegend=_is_name_visible
    ))

  def _draw_point(self, _name, _point, _size, _color):
    self.fig.add_trace(go.Scatter3d(
      name=_name,
      x=[_point.x],
      y=[_point.y],
      z=[_point.z],
      mode='markers',
      marker={
        'size': _size,
        'color': _color,
        'opacity': 1.0
      }
    ))

  def draw(self):
    # Add body outline
    points = self.hexapod.body.vertices
    self._draw_lines('body', points + [points[0]], HexapodPlot.LINE_SIZE, HexapodPlot.BODY_COLOR)

    # Add head and center of gravity
    self._draw_point('cog', self.hexapod.body.cog, HexapodPlot.COG_SIZE, HexapodPlot.COG_COLOR)
    self._draw_point('head', self.hexapod.body.head, HexapodPlot.HEAD_SIZE, HexapodPlot.BODY_COLOR)

    # Draw legs
    for leg in self.hexapod.legs:
      points = [leg.p0, leg.p1, leg.p2, leg.p3]
      self._draw_lines('leg', points, HexapodPlot.LINE_SIZE, HexapodPlot.LEG_COLOR, False)
    return self.fig
  
  def figure(self):
    return self.fig

  def update(self, _hexapod):
    self.hexapod = _hexapod
    
    #body
    points = self.hexapod.body.vertices + [self.hexapod.body.vertices[0]]
    self.fig['data'][0]['x'] = [point.x for point in points]
    self.fig['data'][0]['y'] = [point.y for point in points]
    self.fig['data'][0]['z'] = [point.z for point in points]

    self.fig['data'][2]['x'] = [self.hexapod.body.head.x]
    self.fig['data'][2]['y'] = [self.hexapod.body.head.y]
    self.fig['data'][2]['z'] = [self.hexapod.body.head.z]
    
    # legs
    n = [i for i in range(3, 9)]
    
    for n, leg in zip(n, self.hexapod.legs):
      points = [leg.p0, leg.p1, leg.p2, leg.p3]
      self.fig['data'][n]['x'] = [point.x for point in points]
      self.fig['data'][n]['y'] = [point.y for point in points]
      self.fig['data'][n]['z'] = [point.z for point in points]    
    
    return self.fig