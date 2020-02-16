import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import json

from app import app

from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import NAMES_LEG, NAMES_JOINT, BASE_HEXAPLOT

from widgets.measurements import INPUT_LENGTHS, SECTION_INPUT_LENGTHS, INPUT_LENGTHS_IDs
from widgets.jointsliders import SECTION_LEG_SLIDERS
from widgets.sectioning import make_section_type4, make_section_type3

PLOTTER = BASE_HEXAPLOT

# hidden values of legs
SECTION_LEG_POSES = html.Div([html.Div(id='pose-{}'.format(leg_name), style={'display': 'none'}) for leg_name in NAMES_LEG])

# -----------
# LAYOUT
# -----------
layout = html.Div([

  html.Div([
    dcc.Graph(id='graph-hexapod', style={'width': '45%'}),

    html.Div([

      html.H4('Joint Angles (Pose of each Leg)'),
      SECTION_LEG_SLIDERS,
      html.Br(),

      html.H4('Hexapod Robot Measurements'),
      SECTION_INPUT_LENGTHS,
      html.Br(),

      ], style={'width': '55%'}),
    ], style={'display': 'flex'}
  ),

  html.Br(),

  #html.Div(id='camera-values-from-graph'),  
  SECTION_LEG_POSES, 
  html.Div(id='hexapod-measurements-values', style={'display': 'none'}),
  #html.Div(id='camera-view-values', style={'display': 'none'})
])

# -----------
# Hexapod Measurements CALLBACK
# -----------
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

# -------
# LEG CALLBACKS
# -----------
# 0
@app.callback(
  Output('pose-right-middle', 'children'),
  [Input('slider-right-middle-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_right_middle(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 1
@app.callback(
  Output('pose-right-front', 'children'),
  [Input('slider-right-front-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_right_front(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 2
@app.callback(
  Output('pose-left-front', 'children'),
  [Input('slider-left-front-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_left_front(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 3
@app.callback(
  Output('pose-left-middle', 'children'),
  [Input('slider-left-middle-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_left_middle(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 4
@app.callback(
  Output('pose-left-back', 'children'),
  [Input('slider-left-back-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_left_back(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 5
@app.callback(
  Output('pose-right-back', 'children'),
  [Input('slider-right-back-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_right_back(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# front          x2          x1
#                 \         /
#                  *---*---*
#                 /    |    \
#                /     |     \
#               /      |      \
# middle  x3 --*------cog------*-- x0
#               \      |      /
#                \     |     /
#                 \    |    /
# back             *---*---*
#                 /         \
#                x4         x5
#               left       right
# -------
# FIGURE/GRAPH CALLBACK
# -----------
INPUT_ALL = [Input('pose-{}'.format(leg), 'children') for leg in NAMES_LEG] + \
  [Input(name, 'children') for name in ['hexapod-measurements-values']]
@app.callback(
  Output('graph-hexapod', 'figure'),
  INPUT_ALL, 
  [State('graph-hexapod', 'relayoutData')]
)
def update_graph(rm, rf, lf, lm, lb, rb, measurements, relayout_data):

  if measurements is None:
    raise PreventUpdate

  measurements = json.loads(measurements)

  f, s, m = measurements['front'], measurements['side'], measurements['middle'],
  h, k, a = measurements['coxia'], measurements['femur'], measurements['tibia'],

  virtual_hexapod = VirtualHexapod(h, k, a, f, m, s)
  
  poses = [rm, rf, lf, lm, lb, rb]
  for leg, pose in zip(virtual_hexapod.legs, poses):
    try:
      pose = json.loads(pose)
      alpha, beta, gamma = pose['coxia'], pose['femur'], pose['tibia']
      leg.change_pose(alpha, beta, gamma)
    except:
      print(pose)

  fig = PLOTTER.update(virtual_hexapod, PLOTTER.fig)

  if relayout_data and 'scene.camera' in relayout_data:
    camera = relayout_data['scene.camera']
    print(camera)
    fig = PLOTTER.change_camera_view(camera, fig)

  return fig
