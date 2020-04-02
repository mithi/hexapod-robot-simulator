from copy import deepcopy
from hexapod.const import HEXAPOD_POSE
import numpy as np

def compute_alpha(body_point, foot_point, coxia_axis):
  #                       * foot_point
  #                      /
  #                     /
  #        alpha       / alpha wrt world
  # <-----------------*----------------->
  # coxia_axis      body_point        world_axis
  #
  c = np.sqrt((foot_point.x - body_point.x)**2 + (foot_point.y - body_point.y)**2)
  alpha_wrt_world = np.arcsin((foot_point.x - body_point.x) / c)
  alpha = alpha_wrt_world - coxia_axis
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
  tx = end_x * hexapod.mid
  ty = end_y * hexapod.side
  tz = end_z * hexapod.tibia

  hexapod.detach_body_rotate_and_translate(rot_x, rot_y, rot_z, tx, ty, tz)
  poses = deepcopy(HEXAPOD_POSE)

  for i in range(hexapod.LEG_COUNT):
    body_point = hexapod.body.vertices[i]
    foot_point = hexapod.legs[i].foot_tip()
    coxia_axis = hexapod.body.COXIA_AXES[i]
    alpha = compute_alpha(body_point, foot_point, coxia_axis)
    #poses[i]['coxia']= alpha

  #hexapod.update(poses)

  return hexapod, poses
