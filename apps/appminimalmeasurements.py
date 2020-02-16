import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

import json
import plotly.graph_objs as go

from widgets.camview import SECTION_INPUT_CAMVIEW, CAMVIEW_INPUT_IDs

from hexapod.const import BASE_HEXAPOD, BASE_HEXAPLOT
from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot

from sectioning import make_section_type4, make_section_type3

from app import app

hexaplot = BASE_HEXAPLOT
virtual_hexapod = BASE_HEXAPOD

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

@app.callback(
  Output('camera-view-values', 'children'),
  [Input(input_id, 'value') for input_id in CAMVIEW_INPUT_IDs]
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
  fig = hexaplot.fig

  hexaplot.change_camera_view(json.loads(camera), fig)

  for leg in virtual_hexapod.legs:
    leg.change_pose(alpha, beta, gamma)

  fig = hexaplot.update(virtual_hexapod, fig)
  return fig