import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import NAMES_LEG, NAMES_JOINT, BASE_PLOTTER
from hexapod.figure_template import HEXAPOD_FIGURE

from widgets.measurements import SECTION_LENGTHS_CONTROL, INPUT_LENGTHS, INPUT_LENGTHS_IDs
from widgets.jointsliders import SECTION_POSE_CONTROL
from widgets.sectioning import make_section_type4, make_section_type3

import json
from app import app

# *********************
# *  LAYOUT           *
# *********************
HIDDEN_LEG_POSES = [html.Div(id='pose-{}'.format(leg_name), style={'display': 'none'}) for leg_name in NAMES_LEG]
HIDDEN_LENGTHS = [html.Div(id='hexapod-measurements-values', style={'display': 'none'})]
HIDDEN_LEG_POSES_ALL = [html.Div(id='hexapod-poses-values', style={'display': 'none'})]
HIDDEN_DIVS = HIDDEN_LEG_POSES + HIDDEN_LENGTHS +  HIDDEN_LEG_POSES_ALL

layout = html.Div([
  html.Div(HIDDEN_DIVS),
  html.Div([
    dcc.Graph(id='graph-hexapod', style={'width': '45%'}),
    html.Div([SECTION_POSE_CONTROL, SECTION_LENGTHS_CONTROL], style={'width': '55%'})],
    style={'display': 'flex'}
  ),
])

# *********************
# *  CALLBACKS        *
# *********************

# -------------------
# Listen if the robot measurements are updated
# -------------------
@app.callback(
  Output('hexapod-measurements-values', 'children'),
  [Input(input_id, 'value') for input_id in INPUT_LENGTHS_IDs]
)
def update_hexapod_measurements(fro, sid, mid, cox, fem, tib):
  measurements = {
    'front': fro or 0,
    'side': sid or 0,
    'middle': mid or 0,

    'coxia': cox or 0,
    'femur': fem or 0,
    'tibia': tib or 0, 
  }

  return json.dumps(measurements)

#         x2          x1
#          \         /
#           *---*---*
#          /    |    \
#         /     |     \
#        /      |      \
#  x3 --*------cog------*-- x0
#        \      |      /
#         \     |     /
#          \    |    /
#           *---*---*
#          /         \
#         x4         x5

# -------------------
# Listen if a leg pose is updated
# -------------------
def leg_inputs(prefix):
  return [Input('slider-{}-{}'.format(prefix, joint), 'value') for joint in NAMES_JOINT]

def leg_output(prefix):
  return Output('pose-{}'.format(prefix), 'children')

def leg_json(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

@app.callback(leg_output('right-middle'), leg_inputs('right-middle'))
def update_right_middle(coxia, femur, tibia):
  return leg_json(coxia, femur, tibia)

@app.callback(leg_output('right-front'), leg_inputs('right-front'))
def update_right_front(coxia, femur, tibia):
  return leg_json(coxia, femur, tibia)

@app.callback(leg_output('left-front'), leg_inputs('left-front'))
def update_left_front(coxia, femur, tibia):
  return leg_json(coxia, femur, tibia)

@app.callback(leg_output('left-middle'), leg_inputs('left-middle'))
def update_left_middle(coxia, femur, tibia):
  return leg_json(coxia, femur, tibia)

@app.callback(leg_output('left-back'), leg_inputs('left-back'))
def update_left_back(coxia, femur, tibia):
  return leg_json(coxia, femur, tibia)

@app.callback(leg_output('right-back'), leg_inputs('right-back'))
def update_right_back(coxia, femur, tibia):
  return leg_json(coxia, femur, tibia)

INPUT_LEGS = [Input('pose-{}'.format(leg), 'children') for leg in NAMES_LEG]
@app.callback(
  Output('hexapod-poses-values', 'children'),
  INPUT_LEGS
)
def update_hexapod_pose_values(rm, rf, lf, lm, lb, rb):
  poses = [rm, rf, lf, lm, lb, rb]
  poses_json = {}

  for i, name, pose in zip(range(6), NAMES_LEG, poses):
    try:
      pose = json.loads(pose)
      pose['name'] = name
      pose['id'] = i
      poses_json[i] = pose
    except:
      print("can't parse:", pose)

  return json.dumps(poses_json)
    

# -------------------
# Listen if we need to update Graph
# -------------------
INPUT_ALL = [Input(name, 'children') for name in ['hexapod-poses-values', 'hexapod-measurements-values']]
@app.callback(
  Output('graph-hexapod', 'figure'),
  INPUT_ALL, 
  [State('graph-hexapod', 'relayoutData'), State('graph-hexapod', 'figure')]
)
def update_graph(poses_json, measurements_json, relayout_data, figure):

  if figure is None:
    return HEXAPOD_FIGURE

  if measurements_json is None:
    raise PreventUpdate

  # Make base hexapod model given body measurements
  measurements = json.loads(measurements_json)
  virtual_hexapod = VirtualHexapod(measurements)
  
  # Configure the pose of the hexapod given joint angles
  if poses_json is not None:
    try:
      poses = json.loads(poses_json)
    except:
      print("can't parse:", poses)
    
    virtual_hexapod.update(poses)

  # Update the plot to reflect pose of hexapod
  figure = BASE_PLOTTER.update(figure, virtual_hexapod)

  # Use current camera view to display plot
  if relayout_data and 'scene.camera' in relayout_data:
    camera = relayout_data['scene.camera']
    figure = BASE_PLOTTER.change_camera_view(figure, camera)

  return figure
