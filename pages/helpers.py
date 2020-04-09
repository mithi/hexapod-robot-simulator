from hexapod.const import BASE_PLOTTER
from settings import PRINT_POSE_IN_TERMINAL
from hexapod.const import HEXAPOD_POSE, NAMES_LEG
from copy import deepcopy

poses = deepcopy(HEXAPOD_POSE)
def make_pose(alpha, beta, gamma):

  for k, _ in poses.items():
    poses[k] = {
      'id': k,
      'name': NAMES_LEG[k],
      'coxia': alpha,
      'femur': beta,
      'tibia': gamma,
    }
  return poses

def change_camera_view(figure, relayout_data):
  # Use current camera view to display plot
  if relayout_data and 'scene.camera' in relayout_data:
    camera = relayout_data['scene.camera']
    BASE_PLOTTER.change_camera_view(figure, camera)

  return figure



def format_info(
    dimensions,
    start_hip_stance,
    start_leg_stance,
    percent_x,
    percent_y,
    percent_z,
    rot_x,
    rot_y,
    rot_z):
  return f'''
+----------------+------------+------------+------------+
| rot.x: {rot_x:<+7.2f} | x: {percent_x:<+5.2f} % | coxia: {dimensions['coxia']:3d} | fro: {dimensions['front']:5d} |
| rot.y: {rot_y:<+7.2f} | y: {percent_y:<+5.2f} % | femur: {dimensions['femur']:3d} | sid: {dimensions['side']:5d} |
| rot.z: {rot_z:<+7.2f} | z: {percent_z:<+5.2f} % | tibia: {dimensions['tibia']:3d} | mid: {dimensions['middle']:5d} |
+----------------+------------+------------+------------+
| hip_stance: {start_hip_stance:<+6.2f} | leg_stance: {start_leg_stance:<+6.2f} |
+--------------------+--------------------+
'''


def update_display_message(info, poses, alert):
  # Update display message
  if poses:
    text = add_poses_to_text(info, poses)
  else:
    text = add_alert_to_text(info, alert)

  return text


def add_poses_to_text(postfix_text, poses):
  message = f'''
+----------------+------------+------------+------------+
| leg name       | coxia      | femur      | tibia      |
+----------------+------------+------------+------------+'''
  for pose in poses.values():
    message += f'''
| {pose['name']:14} | {pose['coxia']:<+10.2f} | {pose['femur']:<+10.2f} | {pose['tibia']:<+10.2f} |'''

  return message + postfix_text


def add_alert_to_text(postfix_text, alert):
  return f'''
❗❗❗ALERT❗❗❗
⚠️ {alert} 🔴
{postfix_text}'''