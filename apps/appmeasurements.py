import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import plotly.graph_objs as go

from hexapod import Point, Linkage, Hexagon, VirtualHexapod, HexapodPlot
from app import app


# -----------
# Sliders 
# -----------
SLIDER_ANGLE_MARKS = {tick: str(tick) for tick in [-135, -90, -45, 0, 45, 90, 135]}

SLIDER_ALPHA = dcc.Slider(id='slider-alpha', min=-135, max=135, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_BETA = dcc.Slider(id='slider-beta', min=-135, max=135, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_GAMMA = dcc.Slider(id='slider-gamma', min=-135, max=135, marks=SLIDER_ANGLE_MARKS, value=0, step=5)

SLIDER_MARKS = {tick: str(tick) for tick in [0, 20, 40, 60, 80, 100]}

SLIDER_FRONT = dcc.Slider(id='slider-front', min=0, max=100, marks=SLIDER_MARKS, value=50)
SLIDER_SIDE = dcc.Slider(id='slider-side', min=0, max=100, marks=SLIDER_MARKS, value=50)
SLIDER_MIDDLE = dcc.Slider(id='slider-middle', min=0, max=100, marks=SLIDER_MARKS, value=50)

SLIDER_COXIA = dcc.Slider(id='slider-coxia', min=0, max=100, marks=SLIDER_MARKS, value=50)
SLIDER_FEMUR = dcc.Slider(id='slider-femur', min=0, max=100, marks=SLIDER_MARKS, value=50)
SLIDER_TIBIA = dcc.Slider(id='slider-tibia', min=0, max=100, marks=SLIDER_MARKS, value=50)

SLIDERS = [
  SLIDER_ALPHA,
  SLIDER_BETA,
  SLIDER_GAMMA,
  SLIDER_FRONT,
  SLIDER_SIDE,
  SLIDER_MIDDLE,
  SLIDER_COXIA,
  SLIDER_FEMUR,
  SLIDER_TIBIA,
]

# -----------
# LAYOUT
# -----------
layout = html.Div([
  dcc.Graph(id='hexapod-plot'),
  html.Div(id='sliders', children=SLIDERS),
  html.Div(id='variables', style={'display': 'none'}),
  html.Div(id='display-variables'),
])

# -----------
# CALLBACKS
# -----------
SLIDER_IDs = [
  'slider-alpha', 
  'slider-beta', 
  'slider-gamma',
  'slider-front', 
  'slider-side', 
  'slider-middle',
  'slider-coxia', 
  'slider-femur', 
  'slider-tibia',
]

@app.callback(
  Output('variables', 'children'),
  [Input(i, 'value') for i in SLIDER_IDs]
)
def update_variable(alpha, beta, gamma, f, s, m, h, k, a):
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

@app.callback(
  Output('display-variables', 'children'),
  [Input('variables', 'children')]
)
def display_variables(pose_params):
  p = json.loads(pose_params)
  return dcc.Markdown('# HELLO! {}'.format(str(p)))

@app.callback(
  Output('hexapod-plot', 'figure'),
  [Input(slider_id, 'value') for slider_id in SLIDER_IDs]
)
def update_hexapod_plot(alpha, beta, gamma, f, s, m, h, k, a):
  virtual_hexapod = VirtualHexapod(h, k, a, f, s, m)
  hexaplot = HexapodPlot(virtual_hexapod)

  for leg in virtual_hexapod.legs:
    leg.change_pose(alpha, beta, gamma)
  fig = hexaplot.update(virtual_hexapod)
  return fig
