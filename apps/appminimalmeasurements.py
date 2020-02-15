import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

import json
import plotly.graph_objs as go

from hexapod import Point, Linkage, Hexagon, VirtualHexapod, HexapodPlot
from app import app

FRONT_LENGTH = 60
SIDE_LENGTH = 60
MID_LENGTH = 90
HIP_LENGTH = 60
KNEE_LENGTH = 60
ANKLE_LENGTH = 60

virtual_hexapod = VirtualHexapod(HIP_LENGTH, KNEE_LENGTH, ANKLE_LENGTH, FRONT_LENGTH, MID_LENGTH, SIDE_LENGTH)
hexaplot = HexapodPlot(virtual_hexapod)

# -----------
# INPUTS
# -----------

SLIDER_ANGLE_MARKS = {tick: str(tick) for tick in [-90, -45, 0, 45, 90]}

SLIDER_ALPHA = dcc.Slider(id='2-slider-alpha', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_BETA = dcc.Slider(id='2-slider-beta', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_GAMMA = dcc.Slider(id='2-slider-gamma', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)

NUMBER_INPUT_UP_X = dcc.Input(id='camera-up-x', type='number', value=0.0, step=0.005, style={'marginRight': '5%', 'width': '95%'})
NUMBER_INPUT_UP_Y = dcc.Input(id='camera-up-y', type='number', value=0.0, step=0.005, style={'marginRight': '5%', 'width': '95%'})
NUMBER_INPUT_UP_Z = dcc.Input(id='camera-up-z', type='number', value=1.0, step=0.005, style={'marginRight': '5%', 'width': '95%'})

NUMBER_INPUT_CENTER_X = dcc.Input(id='camera-center-x', type='number', value=-0.05, step=0.005, style={'marginRight': '5%', 'width': '95%'})
NUMBER_INPUT_CENTER_Y = dcc.Input(id='camera-center-y', type='number', value=0.0, step=0.005, style={'marginRight': '5%', 'width': '95%'})
NUMBER_INPUT_CENTER_Z = dcc.Input(id='camera-center-z', type='number', value=-0.1, step=0.005, style={'marginRight': '5%', 'width': '95%'})

NUMBER_INPUT_EYE_X = dcc.Input(id='camera-eye-x', type='number', value=0.35, step=0.005, style={'marginRight': '5%', 'width': '95%'})
NUMBER_INPUT_EYE_Y = dcc.Input(id='camera-eye-y', type='number', value=0.7, step=0.005, style={'marginRight': '5%', 'width': '95%'})
NUMBER_INPUT_EYE_Z = dcc.Input(id='camera-eye-z', type='number', value=0.5, step=0.005, style={'marginRight': '5%', 'width': '95%'})


SLIDERS = [
  SLIDER_ALPHA,
  SLIDER_BETA,
  SLIDER_GAMMA,
]

# -----------
# PARTIALS
# -----------
def make_thirds_div(name1, name2, name3, div1, div2, div3):
  return html.Div([
    html.Div([html.Label(name1), div1], style={'width': '33%'}),
    html.Div([html.Label(name2), div2], style={'width': '33%'}),
    html.Div([html.Label(name3), div3], style={'width': '33%'}),
    ],
    style={'display': 'flex'}
  )

section_input_up = make_thirds_div('up x', 'up y', 'up z', NUMBER_INPUT_UP_X, NUMBER_INPUT_UP_Y, NUMBER_INPUT_UP_Z)
section_input_center = make_thirds_div('center x', 'center y', 'center z', NUMBER_INPUT_CENTER_X, NUMBER_INPUT_CENTER_Y, NUMBER_INPUT_CENTER_Z)
section_input_eye = make_thirds_div('eye x', 'eye y', 'eye z', NUMBER_INPUT_EYE_X, NUMBER_INPUT_EYE_Y, NUMBER_INPUT_EYE_Z)

section_input_camera = html.Div([
  html.Div(section_input_up, style={'width': '33%'}),
  html.Div(section_input_center, style={'width': '33%'}),
  html.Div(section_input_eye, style={'width': '33%'}),
  ],
  style={'display': 'flex'}
)

# -----------
# LAYOUT
# -----------
layout = html.Div([
  dcc.Graph(id='2-hexapod-plot'),
  html.Br(),

  html.H4('Camera View Controls'),
  section_input_camera, 
  html.Br(),

  html.H4('Leg Angles'),
  html.Div(id='2-sliders', children=SLIDERS),
  html.Br(),
])

# -----------
# CALLBACKS
# -----------
INPUT_IDs = [
  'camera-up-x',
  'camera-up-y',
  'camera-up-z',

  'camera-center-x',
  'camera-center-y',
  'camera-center-z',

  'camera-eye-x',
  'camera-eye-y',
  'camera-eye-z',

  '2-slider-alpha', 
  '2-slider-beta', 
  '2-slider-gamma',
]
@app.callback(
  Output('2-hexapod-plot', 'figure'),
  [Input(slider_id, 'value') for slider_id in INPUT_IDs]
)
def update_hexapod_plot(up_x, up_y, up_z, center_x, center_y, center_z, eye_x, eye_y, eye_z, alpha, beta, gamma):
  
  camera = {
    'up': {'x': up_x or 0, 'y': up_y or 0, 'z': up_z or 0},
    'center': {'x': center_x or 0, 'y': center_y or 0, 'z': center_z or 0},
    'eye': {'x': (eye_x or 0), 'y': (eye_y or 0), 'z': (eye_z or 0)}
  }

  hexaplot.change_camera_view(camera)

  for leg in virtual_hexapod.legs:
    leg.change_pose(alpha, beta, gamma)
  fig = hexaplot.update(virtual_hexapod)
  return fig