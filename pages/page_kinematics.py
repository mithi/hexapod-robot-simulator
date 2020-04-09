from settings import WHICH_POSE_CONTROL_UI, PRINT_POSE_IN_TERMINAL

if WHICH_POSE_CONTROL_UI == 1:
  from widgets.pose_control.generic_slider_ui import SECTION_POSE_CONTROL
elif WHICH_POSE_CONTROL_UI == 2:
  from widgets.pose_control.generic_input_ui import SECTION_POSE_CONTROL
else:
  from widgets.pose_control.generic_daq_slider_ui import SECTION_POSE_CONTROL

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, BASE_FIGURE, NAMES_LEG, NAMES_JOINT
from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL, DIMENSION_INPUTS

from copy import deepcopy
import json
from app import app
from pages.shared_callbacks import INPUT_DIMENSIONS_JSON, HIDDEN_BODY_DIMENSIONS
from pages import helpers

# *********************
# *  LAYOUT           *
# *********************
ID_POSES_DIV = 'hexapod-poses-values'
HIDDEN_JOINT_POSES = html.Div(id=ID_POSES_DIV, style={'display': 'none'})
SECTION_CONTROLS = [SECTION_DIMENSION_CONTROL, SECTION_POSE_CONTROL]

layout = html.Div([
  html.Div(SECTION_CONTROLS, style={'width': '45%'}),
  dcc.Graph(id='graph-hexapod', style={'width': '55%'}),
  HIDDEN_JOINT_POSES,
  HIDDEN_BODY_DIMENSIONS
  ],
  style={'display': 'flex'}
)

# *********************
# *  CALLBACKS        *
# *********************
INPUT_POSES_JSON = Input(ID_POSES_DIV, 'children')
OUTPUT = Output('graph-hexapod', 'figure')
INPUTS = [INPUT_DIMENSIONS_JSON, INPUT_POSES_JSON]
STATES = [State('graph-hexapod', 'relayoutData'), State('graph-hexapod', 'figure')]
@app.callback(OUTPUT, INPUTS, STATES)
def update_kinematics_page(dimensions_json, poses_json, relayout_data, figure):

  if figure is None:
    return BASE_FIGURE

  dimensions = helpers.load_dimensions(dimensions_json)
  virtual_hexapod = VirtualHexapod(dimensions)

  poses = json.loads(poses_json)
  virtual_hexapod.update(poses)
  BASE_PLOTTER.update(figure, virtual_hexapod)
  helpers.change_camera_view(figure, relayout_data)
  return figure

# -------------------
# Listen if we need to update pose (IE one of the leg's pose is updated)
# -------------------
def leg_inputs(leg_name):
  return [Input(f'input-{leg_name}-{joint_name}', 'value') for joint_name in NAMES_JOINT]

OUTPUT_POSES = Output(ID_POSES_DIV, 'children')
INPUTS_POSES = []
for leg_name in NAMES_LEG:
  INPUTS_POSES += leg_inputs(leg_name)

@app.callback(OUTPUT_POSES, INPUTS_POSES)
def update_hexapod_pose_values(
  rmc, rmf, rmt,
  rfc, rff, rft,
  lfc, lff, lft,
  lmc, lmf, lmt,
  lbc, lbf, lbt,
  rbc, rbf, rbt,
  ):

  return json.dumps({
    0: {"coxia": rmc, "femur": rmf, "tibia": rmt, "name": "right-middle", "id": 0},
    1: {"coxia": rfc, "femur": rff, "tibia": rft, "name": "right-front", "id": 1},
    2: {"coxia": lfc, "femur": lff, "tibia": lft, "name": "left-front", "id": 2},
    3: {"coxia": lmc, "femur": lmf, "tibia": lmt , "name": "left-middle", "id": 3},
    4: {"coxia": lbc, "femur": lbf, "tibia": lbt, "name": "left-back", "id": 4},
    5: {"coxia": rbc, "femur": rbf, "tibia": rbt , "name": "right-back", "id": 5}
  })
