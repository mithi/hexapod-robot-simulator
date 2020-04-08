from settings import RECOMPUTE_HEXAPOD, PRINT_POSE_IN_TERMINAL
from pages import helpers

import numpy as np
from copy import deepcopy
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, HEXAPOD_FIGURE
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
  percent_x,
  percent_y,
  percent_z,
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

  no_leg_dimensions = coxia is None or femur is None or tibia is None
  no_body_dimensions = front is None or side is None or mid is None
  if no_leg_dimensions or no_body_dimensions:
    raise PreventUpdate

  info = helpers.format_info( start_hip_stance, start_leg_stance,
    percent_x, percent_y, percent_z, rot_x, rot_y, rot_z, front,
    side, mid, coxia, femur, tibia)

  if figure is None:
    return dcc.Markdown(f'```{info}```'), HEXAPOD_FIGURE

  # ***********************************
  # COMPUTE POSES AND UPDATE FIGURE WITH INVERSE KINEMATICS
  # ***********************************
  hexapod = VirtualHexapod().new(front, mid, side, coxia, femur, tibia)

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
  return dcc.Markdown(f'```{text}```'), figure
