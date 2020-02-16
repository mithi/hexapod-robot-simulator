import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import plotly.graph_objs as go

from hexapod import VirtualHexapod
from hexaplot import HexapodPlot
from sectioning import make_section_type3
from measurementwidgets import INPUT_LENGTHS, SECTION_INPUT_LENGTHS, INPUT_LENGTHS_IDs

from const import BASE_HEXAPLOT

from app import app

plotter = BASE_HEXAPLOT

# -----------
# Sliders 
# -----------
SLIDER_ANGLE_MARKS = {tick: str(tick) for tick in [-90, -45, 0, 45, 90]}

SLIDER_ALPHA = dcc.Slider(id='slider-alpha', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_BETA = dcc.Slider(id='slider-beta', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_GAMMA = dcc.Slider(id='slider-gamma', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)

# -----------
# SECTIONS AND LAYOUT
# -----------
section_sliders_angles = make_section_type3(SLIDER_ALPHA, SLIDER_BETA, SLIDER_GAMMA, 'Alpha', 'Beta', 'Gamma')

section_hexapod = html.Div([
  html.Div(dcc.Graph(id='hexapod-plot'), style={'width': '50%'}),
  html.Div([SECTION_INPUT_LENGTHS, section_sliders_angles], style={'width': '40%'}),
  html.Div(id='display-variables', style={'width': '10%'}),
  ], 
  style={'display': 'flex'})

layout = html.Div([
  html.H3('Customization'),
  section_hexapod,
  html.Div(id='variables', style={'display': 'none'}),
])

# -----------
# CALLBACKS
# -----------
INPUT_IDs = ['slider-alpha', 'slider-beta', 'slider-gamma'] + INPUT_LENGTHS_IDs
@app.callback(
  Output('variables', 'children'),
  [Input(i, 'value') for i in INPUT_IDs]
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
  s = ""
  for k, v in p.items():
    s += "- `{}: {}` \n".format(k, v)
  
  return dcc.Markdown(s)

@app.callback(
  Output('hexapod-plot', 'figure'),
  [Input(i, 'value') for i in INPUT_IDs]
)
def update_hexapod_plot(alpha, beta, gamma, f, s, m, h, k, a):
  virtual_hexapod = VirtualHexapod(h, k, a, f, m, s)
  fig = plotter.fig

  for leg in virtual_hexapod.legs:
    leg.change_pose(alpha, beta, gamma)

  fig = plotter.update(virtual_hexapod, fig)
  return fig
