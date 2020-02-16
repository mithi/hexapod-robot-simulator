import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from widgets.sectioning import make_section_type3
from widgets.measurements import INPUT_LENGTHS, SECTION_INPUT_LENGTHS, INPUT_LENGTHS_IDs
from widgets.misc import SECTION_SLIDERS_TEST, SLIDERS_TEST_IDs

from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import BASE_HEXAPLOT

import json
from app import app

plotter = BASE_HEXAPLOT

# -----------
# LAYOUT
# -----------
section_hexapod = html.Div([
  html.Div(dcc.Graph(id='hexapod-plot'), style={'width': '50%'}),
  html.Div([SECTION_INPUT_LENGTHS, SECTION_SLIDERS_TEST], style={'width': '40%'}),
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
INPUT_IDs = SLIDERS_TEST_IDs + INPUT_LENGTHS_IDs
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
