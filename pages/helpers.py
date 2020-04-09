import dash_core_components as dcc
from hexapod.const import BASE_PLOTTER
from settings import PRINT_POSE_IN_TERMINAL
from hexapod.const import HEXAPOD_POSE, NAMES_LEG, BASE_DIMENSIONS
from copy import deepcopy
import json


def change_camera_view(figure, relayout_data):
  # Use current camera view to display plot
  if relayout_data and 'scene.camera' in relayout_data:
    camera = relayout_data['scene.camera']
    BASE_PLOTTER.change_camera_view(figure, camera)

  return figure


def load_dimensions(dimensions_json):
  try:
    dimensions = json.loads(dimensions_json)
  except:
    dimensions = BASE_DIMENSIONS
  return dimensions


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


def make_monospace(text):
  return dcc.Markdown(f'```{text}```')


def format_info(dimensions, ik_parameters):
  px, py, pz = ik_parameters['percent_x'], ik_parameters['percent_y'], ik_parameters['percent_z']
  rx, ry, rz = ik_parameters['rot_x'] ,ik_parameters['rot_y'] ,ik_parameters['rot_z']

  return f'''
+----------------+------------+------------+------------+
| rot.x: {rx:<+7.2f} | x: {px:<+5.2f} % | coxia: {dimensions['coxia']:3d} | fro: {dimensions['front']:5d} |
| rot.y: {ry:<+7.2f} | y: {py:<+5.2f} % | femur: {dimensions['femur']:3d} | sid: {dimensions['side']:5d} |
| rot.z: {rz:<+7.2f} | z: {pz:<+5.2f} % | tibia: {dimensions['tibia']:3d} | mid: {dimensions['middle']:5d} |
+----------------+------------+------------+------------+
| hip_stance: {ik_parameters['hip_stance']:<+6.2f} | leg_stance: {ik_parameters['leg_stance']:<+6.2f} |
+--------------------+--------------------+
'''


def update_display_message(info, poses, alert):
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