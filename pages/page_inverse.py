from settings import RECOMPUTE_HEXAPOD, PRINT_POSE_IN_TERMINAL

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, BASE_FIGURE
from hexapod.ik_solver import inverse_kinematics_update
from widgets.ik_ui import SECTION_IK, IK_INPUTS
from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL, DIMENSION_INPUTS

import numpy as np
from copy import deepcopy
import json
from app import app
from pages.shared_callbacks import INPUT_DIMENSIONS_JSON, HIDDEN_BODY_DIMENSIONS
from pages import helpers

# *********************
# *  LAYOUT           *
# *********************
SECTION_CONTROLS =[
  SECTION_DIMENSION_CONTROL,
  SECTION_IK,
  html.Div(id='ik-variables')
]

layout = html.Div([
  html.Div(SECTION_CONTROLS, style={'width': '40%'}),
  dcc.Graph(id='graph-hexapod-2', style={'width': '60%'}),
  HIDDEN_BODY_DIMENSIONS
  ],
  style={'display': 'flex'}
)

# *********************
# *  CALLBACKS        *
# *********************
OUTPUTS = [Output('graph-hexapod-2', 'figure'), Output('ik-variables', 'children')]
INPUTS = [INPUT_DIMENSIONS_JSON] + IK_INPUTS
STATES = [State('graph-hexapod-2', 'relayoutData'), State('graph-hexapod-2', 'figure')]
@app.callback(OUTPUTS, INPUTS, STATES)
def update_inverse_page(
  dimensions_json,
  start_hip_stance,
  start_leg_stance,
  percent_x,
  percent_y,
  percent_z,
  rot_x,
  rot_y,
  rot_z,
  relayout_data,
  figure):

  dimensions = helpers.load_dimensions(dimensions_json)

  info = helpers.format_info(dimensions, start_hip_stance, start_leg_stance,
    percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)

  if figure is None:
    return BASE_FIGURE, dcc.Markdown(f'```{info}```')

  # ***********************************
  # COMPUTE POSES AND UPDATE FIGURE WITH INVERSE KINEMATICS
  # ***********************************
  hexapod = VirtualHexapod(dimensions)

  if RECOMPUTE_HEXAPOD:
    hexapod_clone = deepcopy(hexapod)

  hexapod.update_stance(start_hip_stance, start_leg_stance)
  hexapod, poses, alert = inverse_kinematics_update(hexapod, rot_x, rot_y, rot_z, percent_x, percent_y, percent_z)

  if not RECOMPUTE_HEXAPOD:
    BASE_PLOTTER.update(figure, hexapod)
  else:
    if poses:
      hexapod_clone.update(poses)
      hexapod_clone.move_xyz(percent_x, percent_y, percent_z)
      BASE_PLOTTER.update(figure, hexapod_clone)
    else:
      BASE_PLOTTER.update(figure, hexapod)

  text = helpers.update_display_message(info, poses, alert)
  figure = helpers.change_camera_view(figure, relayout_data)
  return figure, dcc.Markdown(f'```{text}```')
