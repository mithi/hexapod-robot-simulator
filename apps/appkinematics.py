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
HIDDEN_TOES = [html.Div(id='toes',  style={'display': 'none'})]

HIDDEN_DIVS = HIDDEN_LEG_POSES + HIDDEN_LENGTHS + HIDDEN_TOES

layout = html.Div([
  html.Div(HIDDEN_DIVS),
  html.Div([
    dcc.Graph(id='graph-hexapod', style={'width': '45%'}),
    html.Div([SECTION_POSE_CONTROL, SECTION_LENGTHS_CONTROL], style={'width': '55%'})],
    style={'display': 'flex'}
  ),
  html.Div(id='display-toes'),
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

@app.callback(Output('display-toes', 'children'), [Input('toes', 'children')])
def display_toes(feet):
  if feet is None:
    return html.H1('No toes to display')
  
  feet = json.loads(feet)['text']
  return dcc.Markdown(feet)

# -------------------
# Listen if we need to update Graph
# -------------------
INPUT_ALL = [Input('pose-{}'.format(leg), 'children') for leg in NAMES_LEG] + \
  [Input(name, 'children') for name in ['hexapod-measurements-values']]
@app.callback(
  [Output('graph-hexapod', 'figure'), Output('toes', 'children')],
  INPUT_ALL, 
  [State('graph-hexapod', 'relayoutData'), State('graph-hexapod', 'figure')]
)
def update_graph(rm, rf, lf, lm, lb, rb, measurements, relayout_data, figure):

  if figure is None:
    return HEXAPOD_FIGURE, None

  if measurements is None:
    raise PreventUpdate

  # make base hexapod model given body measurements
  measurements = json.loads(measurements)

  f, s, m = measurements['front'], measurements['side'], measurements['middle'],
  h, k, a = measurements['coxia'], measurements['femur'], measurements['tibia'],

  virtual_hexapod = VirtualHexapod(h, k, a, f, m, s)
  
  # Configure the pose of the hexapod given joint angles
  poses = [rm, rf, lf, lm, lb, rb]
  for leg, pose in zip(virtual_hexapod.legs, poses):
    try:
      pose = json.loads(pose)
      alpha, beta, gamma = pose['coxia'], pose['femur'], pose['tibia']
      leg.change_pose(alpha, beta, gamma)
    except:
      print(pose)

  figure = BASE_PLOTTER.update(figure, virtual_hexapod)

  # Use current camera view to display plot
  if relayout_data and 'scene.camera' in relayout_data:
    camera = relayout_data['scene.camera']
    figure = BASE_PLOTTER.change_camera_view(figure, camera)

  # Get feet information
  feet, _ = virtual_hexapod.find_feet_on_ground()
  text ='\n'
  for foot in feet:
    text += '- **`{}`** `x:{}, y: {} z: {}` \n'.format(
      foot.name, foot.toe().x, foot.toe().y, foot.toe().z)

  return figure, json.dumps({'text': text})
