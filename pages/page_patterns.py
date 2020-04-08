from settings import PRINT_POSE_IN_TERMINAL
from pages import helpers

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL, DIMENSION_INPUTS
from widgets.alpha_beta_gamma_ui import SECTION_SLIDERS_TEST, SLIDERS_TEST_INPUTS
from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import (
  BASE_PLOTTER,
  NAMES_LEG,
  HEXAPOD_POSE,
  base_figure
)

from copy import deepcopy
import json
from app import app

# -----------
# LAYOUT
# -----------
section_hexapod = html.Div([
  html.Div([
    SECTION_DIMENSION_CONTROL,
    SECTION_SLIDERS_TEST,
    html.Div(id='display-variables'),
  ],
    style={'width': '35%'}
  ),
  html.Div([dcc.Graph(id='hexapod-plot')], style={'width': '65%'}),
  ],
  style={'display': 'flex'}
)

layout = html.Div([
  section_hexapod,
  html.Div(id='variables', style={'display': 'none'}),
])


# -----------
# CALLBACKS
# -----------
INPUTS = SLIDERS_TEST_INPUTS + DIMENSION_INPUTS
@app.callback(
  Output('hexapod-plot', 'figure'),
  INPUTS,
  [State('hexapod-plot', 'relayoutData'), State('hexapod-plot', 'figure')]
)
def update_hexapod_plot(alpha, beta, gamma, f, s, m, h, k, a, relayout_data, figure):

  no_body_dimensions = f is None or s is None or m is None
  no_leg_dimensions = h is None or k is None or a is None
  if no_leg_dimensions or no_body_dimensions:
    raise PreventUpdate

  if figure is None:
    return base_figure()

  virtual_hexapod = VirtualHexapod().new(f, m, s, h, k, a)
  poses = helpers.make_pose(alpha, beta, gamma)
  virtual_hexapod.update(poses)
  BASE_PLOTTER.update(figure, virtual_hexapod)
  helpers.change_camera_view(figure, relayout_data)
  return figure


@app.callback(
  Output('variables', 'children'),
  SLIDERS_TEST_INPUTS + DIMENSION_INPUTS
)
def update_variables(alpha, beta, gamma, f, s, m, h, k, a):
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

  info = f'''```
+----------------+-------------+------------+
| alpha: {p['alpha']:<+7.2f} | front:  {p['front']:3d} | coxia: {p['coxia']:3d} |
| beta:  {p['beta']:<+7.2f} | side:   {p['side']:3d} | femur: {p['femur']:3d} |
| gama:  {p['gamma']:<+7.2f} | middle: {p['middle']:3d} | tibia: {p['tibia']:3d} |
+----------------+-------------+------------+
```'''

  return dcc.Markdown(info)
