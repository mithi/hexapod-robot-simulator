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

SECTION_SLIDERS = html.Div([
  html.Div(html.H6('Leg Angles'), style={'width': '10%'}),
  html.Div([html.Label('alpha'), SLIDER_ALPHA], style={'width': '30%'}),
  html.Div([html.Label('beta'), SLIDER_BETA], style={'width': '30%'}),
  html.Div([html.Label('gamma'), SLIDER_GAMMA], style={'width': '30%'}),
  ],
  style={'display': 'flex'}
)
# -----------
# CAMERA VIEW
# -----------
def make_number_input(_name, _value):
  return dcc.Input(id=_name, type='number', value=_value, step=0.005, style={'marginRight': '5%', 'width': '95%', 'marginBottom': '5%'})

# Camera view adjustment inputs
INPUT_CAMVIEW = {
  'up-x': make_number_input('input-view-up-x', 0.0),
  'up-y': make_number_input('input-view-up-y', 0.0),
  'up-z': make_number_input('input-view-up-z', 1.0),

  'center-x': make_number_input('input-view-center-x', -0.05),
  'center-y': make_number_input('input-view-center-y', 0.0),
  'center-z': make_number_input('input-view-center-z', -0.1),

  'eye-x': make_number_input('input-view-eye-x', 0.35),
  'eye-y': make_number_input('input-view-eye-y', 0.7),
  'eye-z': make_number_input('input-view-eye-z', 0.5),
}

def make_section_type4(div1, div2, div3, div4):
  return html.Div([
    html.Div(div1, style={'width': '13%'}),
    html.Div(div2, style={'width': '29%'}),
    html.Div(div3, style={'width': '29%'}),
    html.Div(div4, style={'width': '29%'}),
    ],
    style={'display': 'flex'}
  )

# section for camera view adjustments
section_input_up = make_section_type4(dcc.Markdown('`(UP)`'), INPUT_CAMVIEW['up-x'], INPUT_CAMVIEW['up-y'], INPUT_CAMVIEW['up-z'])
section_input_center = make_section_type4(dcc.Markdown('`(CNTR)`'), INPUT_CAMVIEW['center-x'], INPUT_CAMVIEW['center-y'], INPUT_CAMVIEW['center-z'])
section_input_eye = make_section_type4(dcc.Markdown('`(EYE)`'), INPUT_CAMVIEW['eye-x'], INPUT_CAMVIEW['eye-y'], INPUT_CAMVIEW['eye-z'])
SECTION_INPUT_CAMVIEW = html.Div([
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

  html.H4('Camera View Adjustment Controls'),
  SECTION_INPUT_CAMVIEW,
  html.Br(),

  SECTION_SLIDERS,
  html.Br(),

  html.Div(id='camera-view-values', style={'display': 'none'}),
])

# -----------
# CALLBACKS
# -----------

INPUT_IDs = [
  'input-view-up-x',
  'input-view-up-y',
  'input-view-up-z',

  'input-view-center-x',
  'input-view-center-y',
  'input-view-center-z',

  'input-view-eye-x',
  'input-view-eye-y',
  'input-view-eye-z',
]
@app.callback(
  Output('camera-view-values', 'children'),
  [Input(input_id, 'value') for input_id in INPUT_IDs]
)
def update_camera_view(up_x, up_y, up_z, center_x, center_y, center_z, eye_x, eye_y, eye_z):
  camera = {
    'up': {'x': up_x or 0, 'y': up_y or 0, 'z': up_z or 0},
    'center': {'x': center_x or 0, 'y': center_y or 0, 'z': center_z or 0},
    'eye': {'x': (eye_x or 0), 'y': (eye_y or 0), 'z': (eye_z or 0)}
  }

  return json.dumps(camera)

INPUT_IDs = [
  '2-slider-alpha', 
  '2-slider-beta', 
  '2-slider-gamma',
]
@app.callback(
  Output('2-hexapod-plot', 'figure'),
  [Input(input_id, 'value') for input_id in INPUT_IDs] + [Input('camera-view-values', 'children')]
)
def update_hexapod_plot(alpha, beta, gamma, camera):
  hexaplot.change_camera_view(json.loads(camera))

  for leg in virtual_hexapod.legs:
    leg.change_pose(alpha, beta, gamma)

  fig = hexaplot.update(virtual_hexapod)
  return fig