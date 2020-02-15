import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
# Sliders 
# -----------
SLIDER_ANGLE_MARKS = {tick: str(tick) for tick in [-90, -45, 0, 45, 90]}

SLIDER_ALPHA = dcc.Slider(id='2-slider-alpha', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_BETA = dcc.Slider(id='2-slider-beta', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_GAMMA = dcc.Slider(id='2-slider-gamma', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)


SLIDERS = [
  SLIDER_ALPHA,
  SLIDER_BETA,
  SLIDER_GAMMA,
]

# -----------
# LAYOUT
# -----------
layout = html.Div([
  dcc.Graph(id='2-hexapod-plot'),
  html.Div(id='2-sliders', children=SLIDERS),
])

# -----------
# CALLBACKS
# -----------
SLIDER_IDs = [
  '2-slider-alpha', 
  '2-slider-beta', 
  '2-slider-gamma',
]

@app.callback(
  Output('2-hexapod-plot', 'figure'),
  [Input(slider_id, 'value') for slider_id in SLIDER_IDs]
)
def update_hexapod_plot(alpha, beta, gamma):
  for leg in virtual_hexapod.legs:
    leg.change_pose(alpha, beta, gamma)
  fig = hexaplot.update(virtual_hexapod)
  return fig
