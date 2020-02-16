import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from widgets.sectioning import make_section_type4, make_section_type3
from widgets.camview import SECTION_INPUT_CAMVIEW, CAMVIEW_INPUT_IDs
from widgets.misc import SECTION_SLIDERS_TEST, SLIDERS_TEST_IDs

from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import BASE_HEXAPOD, BASE_PLOTTER
from hexapod.figure_template import HEXAPOD_FIGURE

import json
from copy import deepcopy

from app import app

# -----------
# LAYOUT
# -----------
layout = html.Div([
  dcc.Graph(id='2-hexapod-plot'),
  html.Br(),

  html.H4('Camera View Adjustment Controls'),
  SECTION_INPUT_CAMVIEW,
  html.Br(),

  SECTION_SLIDERS_TEST,
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

@app.callback(
  Output('2-hexapod-plot', 'figure'),
  [Input(input_id, 'value') for input_id in SLIDERS_TEST_IDs] + [Input('camera-view-values', 'children')],
  [State('2-hexapod-plot', 'figure')]
)
def update_hexapod_plot(alpha, beta, gamma, camera, figure):
  if figure is None:
    return HEXAPOD_FIGURE

  virtual_hexapod = deepcopy(BASE_HEXAPOD)

  for leg in virtual_hexapod.legs:
    leg.change_pose(alpha, beta, gamma)

  if camera is not None:
    figure = BASE_PLOTTER.change_camera_view(json.loads(camera), figure)

  return BASE_PLOTTER.update(virtual_hexapod, figure)
