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
  start_cog_z,
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

  # end_x is  % of middle
  # end_y is % of side
  # end_z is % of tibia

  # Display the parameter values on the screen
  text = dcc.Markdown(f'''
  ```
x: {end_x} | rot.x: {rot_x} | coxia: {coxia} | fro: {front}
y: {end_y} | rot.y: {rot_y} | femur: {femur} | sid: {side}
z: {end_z} | rot.z: {rot_z} | tibia: {tibia} | mid: {mid}
stance: {start_hip_stance} | init.z: {start_cog_z}


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
  virtual_hexapod = VirtualHexapod().new(
    front or 0,
    mid or 0,
    side or 0,
    coxia or 0,
    femur or 0,
    tibia or 0
  )

  # Update pose of hexapod

  # update given start_hipstance
  pose = deepcopy(HEXAPOD_POSE)
  pose[1]["coxia"] = -start_hip_stance # right_front
  pose[2]["coxia"] = start_hip_stance # left_front
  pose[4]["coxia"] = -start_hip_stance # left_back
  pose[5]["coxia"] = start_hip_stance # right_back

  # update pose given start_cog_z
  for key in pose.keys():
    pose[key]["femur"] = -start_cog_z
    pose[key]["tibia"] = start_cog_z


  virtual_hexapod.update(pose)
  tx = end_x * mid
  ty = end_y * side
  tz = end_z * tibia
  virtual_hexapod.detach_body_rotate_and_translate(rot_x, rot_y, rot_z, tx, ty, tz)

  BASE_PLOTTER.update(figure, virtual_hexapod)

  # Use current camera view to display plot
  if relayout_data and 'scene.camera' in relayout_data:
    camera = relayout_data['scene.camera']
    figure = BASE_PLOTTER.change_camera_view(figure, camera)

  return text, figure