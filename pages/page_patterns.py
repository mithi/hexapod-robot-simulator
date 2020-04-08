from settings import PRINT_POSE_IN_TERMINAL
from pages import helpers

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL, DIMENSION_INPUTS
from widgets.alpha_beta_gamma_ui import SECTION_SLIDERS_TEST, SLIDERS_TEST_INPUTS
from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import (
  BASE_PLOTTER,
  NAMES_LEG,
  HEXAPOD_POSE,
  base_figure
)

from copy import deepcopy
import json
from app import app

# -----------
# LAYOUT
# -----------
SECTION_CONTROLS = [
  SECTION_DIMENSION_CONTROL,
  SECTION_SLIDERS_TEST,
  html.Div(id='display-variables'),
]

layout = html.Div([
  html.Div(SECTION_CONTROLS, style={'width': '35%'}),
  dcc.Graph(id='graph-hexapod-3', style={'width': '65%'})],
  style={'display': 'flex'}
)

# -----------
# CALLBACKS
# -----------
OUTPUT = Output('graph-hexapod-3', 'figure')
INPUTS = SLIDERS_TEST_INPUTS + DIMENSION_INPUTS
STATES = [State('graph-hexapod-3', 'relayoutData'), State('graph-hexapod-3', 'figure')]
@app.callback(OUTPUT, INPUTS, STATES)
def update_patterns_page(alpha, beta, gamma, f, s, m, h, k, a, relayout_data, figure):

  no_body_dimensions = f is None or s is None or m is None
  no_leg_dimensions = h is None or k is None or a is None
  if no_leg_dimensions or no_body_dimensions:
    raise PreventUpdate

  if figure is None:
    return base_figure()

  virtual_hexapod = VirtualHexapod().new(f, m, s, h, k, a)
  poses = helpers.make_pose(alpha, beta, gamma)
  virtual_hexapod.update(poses)
  BASE_PLOTTER.update(figure, virtual_hexapod)
  helpers.change_camera_view(figure, relayout_data)
  return figure


OUTPUT = Output('variables', 'children')
@app.callback(OUTPUT, INPUTS)
def update_variables(alpha, beta, gamma, f, s, m, h, k, a):
  return json.dumps({
    'alpha': alpha,
    'beta': beta,
    'gamma': gamma,
    'front': f,
    'side': s,
    'middle': m,
    'coxia': h,
    'femur': k,
    'tibia': a,
  })

