RECOMPUTE_HEXAPOD = False
# The inverse kinematics solver already updates the points of the hexapod
# but if you want to test whether the pose is indeed correct
# ie use the poses returned by the inverse kinematics solve
# set RECOMPUTE_HEXAPOD to true
# otherwise for faster graph/plot updates, set RECOMPUTE_HEXAPOD to False

import numpy as np
from copy import deepcopy
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from hexapod.models import VirtualHexapod
from hexapod.const import (
  BASE_PLOTTER,
  BASE_HEXAPOD,
  HEXAPOD_FIGURE,
  HEXAPOD_POSE
)
from hexapod.ik_solver import inverse_kinematics_update
from widgets.ik_ui import SECTION_IK, IK_INPUTS
from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL, DIMENSION_INPUTS
from app import app

layout = html.Div([
    html.Div([
      html.Label(dcc.Markdown('**INVERSE KINEMATICS CONTROLS**')),
      SECTION_IK,
      html.Br(),
      SECTION_DIMENSION_CONTROL,
      html.Div(id='ik-variables')],
      style={'width': '40%'}),
    dcc.Graph(id='graph-hexapod-2', style={'width': '60%'}),
  ],
  style={'display': 'flex'}
)

INPUTS = IK_INPUTS + DIMENSION_INPUTS
@app.callback(
  [Output('ik-variables', 'children'), Output('graph-hexapod-2', 'figure')],
   INPUTS,
  [State('graph-hexapod-2', 'relayoutData'), State('graph-hexapod-2', 'figure')]
)
def display_variables(
  start_hip_stance,
  start_leg_stance,
  end_x,
  end_y,
  end_z,
  rot_x,
  rot_y,
  rot_z,
  front,
  side,
  mid,
  coxia,
  femur,
  tibia,
  relayout_data,
  figure):

  info = f'''
+----------------+------------+------------+------------+
| rot.x: {rot_x:<+7.2f} | x: {end_x:<+5.2f} % | coxia: {coxia:3d} | fro: {front:5d} |
| rot.y: {rot_y:<+7.2f} | y: {end_y:<+5.2f} % | femur: {femur:3d} | sid: {side:5d} |
| rot.z: {rot_z:<+7.2f} | z: {end_z:<+5.2f} % | tibia: {tibia:3d} | mid: {mid:5d} |
+----------------+------------+------------+------------+
| hip_stance: {start_hip_stance:<+7.2f} |
| leg_stance: {start_leg_stance:<+7.2f} |
+---------------------+
'''

  # If there's no figure, create the default one
  if figure is None:
    print('No hexapod figure')
    hexapod = deepcopy(BASE_HEXAPOD)
    hexapod.update(HEXAPOD_POSE)
    return dcc.Markdown(f'```{info}```'), BASE_PLOTTER.update(HEXAPOD_FIGURE, hexapod)

  # Create a hexapod
  hexapod = VirtualHexapod().new(
    front or 0,
    mid or 0,
    side or 0,
    coxia or 0,
    femur or 0,
    tibia or 0
  )

  # ***********************************
  # COMPUTE POSES AND UPDATE FIGURE WITH INVERSE KINEMATICS
  # ***********************************

  if RECOMPUTE_HEXAPOD:
    hexapod_clone = deepcopy(hexapod)

  hexapod.update_stance(start_hip_stance, start_leg_stance)
  hexapod, poses, alert = inverse_kinematics_update(hexapod, rot_x, rot_y, rot_z, end_x, end_y, end_z)

  if not RECOMPUTE_HEXAPOD:
    BASE_PLOTTER.update(figure, hexapod)
  else:
    if poses:
      hexapod_clone.update(poses)
      BASE_PLOTTER.update(figure, hexapod_clone)
    else:
      BASE_PLOTTER.update(figure, hexapod)

  # ***********************************
  # finalize return values
  # ***********************************

  # Update display message
  if poses:
    text = add_poses_to_text(info, poses)
  else:
    text = add_alert_to_text(info, alert)

  # Use current camera view to display plot
  if relayout_data and 'scene.camera' in relayout_data:
    camera = relayout_data['scene.camera']
    BASE_PLOTTER.change_camera_view(figure, camera)

  return dcc.Markdown(f'```{text}```'), figure


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
