from settings import PRINT_POSE_IN_TERMINAL

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL, DIMENSION_INPUTS
from widgets.leg_patterns_ui import SECTION_SLIDERS_TEST, SLIDERS_TEST_INPUTS
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, BASE_FIGURE, NAMES_LEG

from copy import deepcopy
import json
from app import app
from pages.shared_callbacks import INPUT_DIMENSIONS_JSON, HIDDEN_BODY_DIMENSIONS
from pages import helpers

# *********************
# *  LAYOUT           *
# *********************
ID_POSES_DIV = 'hexapod-poses-values-2'
HIDDEN_JOINT_POSES = html.Div(id=ID_POSES_DIV, style={'display': 'none'})
SECTION_CONTROLS = [SECTION_DIMENSION_CONTROL, SECTION_SLIDERS_TEST]

layout = html.Div([
  html.Div(SECTION_CONTROLS, style={'width': '35%'}),
  dcc.Graph(id='graph-hexapod-3', style={'width': '65%'}),
  HIDDEN_BODY_DIMENSIONS,
  HIDDEN_JOINT_POSES,
  ],
  style={'display': 'flex'}
)

# *********************
# *  CALLBACKS        *
# *********************
INPUT_POSES_JSON = Input(ID_POSES_DIV, 'children')
OUTPUT = Output('graph-hexapod-3', 'figure')
INPUTS = [INPUT_DIMENSIONS_JSON, INPUT_POSES_JSON]
STATES = [State('graph-hexapod-3', 'relayoutData'), State('graph-hexapod-3', 'figure')]
@app.callback(OUTPUT, INPUTS, STATES)
def update_patterns_page(dimensions_json, poses_json, relayout_data, figure):

  if figure is None:
    return BASE_FIGURE

  dimensions = helpers.load_dimensions(dimensions_json)
  virtual_hexapod = VirtualHexapod(dimensions)
  poses = json.loads(poses_json)
  virtual_hexapod.update(poses)
  BASE_PLOTTER.update(figure, virtual_hexapod)
  helpers.change_camera_view(figure, relayout_data)
  return figure

OUTPUT = Output(ID_POSES_DIV, 'children')
INPUTS = SLIDERS_TEST_INPUTS
@app.callback(OUTPUT, INPUTS)
def update_poses_alpha_beta_gamma(alpha, beta, gamma):
  return json.dumps(helpers.make_pose(alpha, beta, gamma))
