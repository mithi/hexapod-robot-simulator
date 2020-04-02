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

SECTION_LEFT = html.Div([
    html.Div([
      html.Label(dcc.Markdown('**INVERSE KINEMATICS CONTROLS**')),
      SECTION_IK,
      SECTION_LENGTHS_CONTROL,
      html.Div(id='ik-variables')],
      style={'width': '47%'}),
    dcc.Graph(id='graph-hexapod-2', style={'width': '53%'}),
  ],
  style={'display': 'flex'}
)


layout = html.Div([
  html.H1('Inverse Kinematics'),
  SECTION_LEFT,
])


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

  # Display the parameter values on the screen
  text = dcc.Markdown(f'''
  ```
x: {end_x} | rot.x: {rot_x} | coxia: {coxia} | fro: {front}
y: {end_y} | rot.y: {rot_y} | femur: {femur} | sid: {side}
z: {end_z} | rot.z: {rot_z} | tibia: {tibia} | mid: {mid}
hip_stance: {start_hip_stance} | leg_stance: {start_leg_stance}


  ```
  '''
  )


  # If there's no figure, create the default one
  if figure is None:
    print('No hexapod figure')
    hexapod = deepcopy(BASE_HEXAPOD)
    hexapod.update(HEXAPOD_POSE)
    return text, BASE_PLOTTER.update(HEXAPOD_FIGURE, hexapod)

  # Create a hexapod
  hexapod = VirtualHexapod().new(
    front or 0,
    mid or 0,
    side or 0,
    coxia or 0,
    femur or 0,
    tibia or 0
  )

  hexapod.update_stance(start_hip_stance, start_leg_stance)
  hexapod, _ = inverse_kinematics_update(hexapod, rot_x, rot_y, rot_z, end_x, end_y, end_z)

  BASE_PLOTTER.update(figure, hexapod)

  # Use current camera view to display plot
  if relayout_data and 'scene.camera' in relayout_data:
    camera = relayout_data['scene.camera']
    figure = BASE_PLOTTER.change_camera_view(figure, camera)

  return text, figure