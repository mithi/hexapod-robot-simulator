from copy import deepcopy
from hexapod.const import HEXAPOD_POSE
import numpy as np
from hexapod.models import VirtualHexapod, Linkage
from hexapod.points import rotx

#def compute_alpha_wrt_world(body_point, foot_point):
  #                       * foot_point
  #                      /
  #                     /
  #        alpha       / alpha wrt world
  # <-----------------*----------------->
  # coxia_axis      body_point        world_axis
  #
#  c = np.sqrt((foot_point.x - body_point.x)**2 + (foot_point.y - body_point.y)**2)
#  alpha= np.arccos((foot_point.x - body_point.x) / c)
#  return alpha

def inverse_kinematics_update(
  hexapod,
  rot_x,
  rot_y,
  rot_z,
  end_x,
  end_y,
  end_z,

):

  tx = end_x * hexapod.mid
  ty = end_y * hexapod.side
  tz = end_z * hexapod.tibia

  hexapod.detach_body_and_coxia_rotate_and_translate(rot_x, rot_y, rot_z, tx, ty, tz)
  #poses = deepcopy(HEXAPOD_POSE)

  return hexapod, None
