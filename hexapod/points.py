import numpy as np

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
  def __init__(self, x, y, z, name=None):
    self.x = x
    self.y = y
    self.z = z
    self.name = name

  def get_point_wrt(self, reference_frame):
    # given frame_ab which is the pose of frame_b wrt frame_a
    # given a point as defined wrt to frame_b
    # return point defined wrt to frame a
    p = np.array([self.x, self.y, self.z, 1])
    p = np.matmul(reference_frame, p)
    return Point(p[0], p[1], p[2])
