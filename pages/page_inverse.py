import numpy as np

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import (
  NAMES_LEG,
  NAMES_JOINT,
  BASE_PLOTTER,
  BASE_HEXAPOD,
  HEXAPOD_FIGURE,
  HEXAPOD_POSE
)

from hexapod.ik_solver import inverse_kinematics_update

from widgets.ik_ui import IK_INPUTS, SECTION_IK
from widgets.measurements import SECTION_LENGTHS_CONTROL, MEASUREMENT_INPUTS
from copy import deepcopy

from app import app

layout = html.Div([
    html.Div([
      html.Label(dcc.Markdown('**INVERSE KINEMATICS CONTROLS**')),
      SECTION_IK,
      html.Br(),
      SECTION_LENGTHS_CONTROL,
      html.Div(id='ik-variables')],
      style={'width': '47%'}),
    dcc.Graph(id='graph-hexapod-2', style={'width': '53%'}),
  ],
  style={'display': 'flex'}
)

INPUTS = IK_INPUTS + MEASUREMENT_INPUTS
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

  text = f'''
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
    return dcc.Markdown(f'```{text}```'), BASE_PLOTTER.update(HEXAPOD_FIGURE, hexapod)

  # Create a hexapod
  hexapod = VirtualHexapod().new(
    front or 0,
    mid or 0,
    side or 0,
    coxia or 0,
    femur or 0,
    tibia or 0
  )
  hexapod_clone = deepcopy(hexapod)

  hexapod.update_stance(start_hip_stance, start_leg_stance)
  hexapod, poses, msg = inverse_kinematics_update(hexapod, rot_x, rot_y, rot_z, end_x, end_y, end_z)
  if msg is not None:
    text = f'''{msg} | {text}'''
    BASE_PLOTTER.update(figure, hexapod)
  else:
    hexapod_clone.update(poses)
    BASE_PLOTTER.update(figure, hexapod_clone)
    text = add_poses_to_text(text, poses)


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