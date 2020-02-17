import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from widgets.sectioning import make_section_type3
from widgets.measurements import SECTION_LENGTHS_CONTROL, INPUT_LENGTHS_IDs
from widgets.camview import SECTION_INPUT_CAMVIEW, CAMVIEW_INPUT_IDs
from widgets.misc import SECTION_SLIDERS_TEST, SLIDERS_TEST_IDs

from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import BASE_PLOTTER
from hexapod.figure_template import HEXAPOD_FIGURE

import json
from app import app

# -----------
# LAYOUT
# -----------
section_hexapod = html.Div([
  html.Div(dcc.Graph(id='hexapod-plot'), style={'width': '50%'}),
  html.Div([SECTION_LENGTHS_CONTROL, SECTION_SLIDERS_TEST], style={'width': '40%'}),
  html.Div(id='display-variables', style={'width': '10%'})], 
  style={'display': 'flex'}
)

layout = html.Div([
  section_hexapod,

  html.H4('Camera View Adjustment Controls'),
  SECTION_INPUT_CAMVIEW,
  html.Br(),

  html.Div(id='camera-view-values', style={'display': 'none'}),
  html.Div(id='variables', style={'display': 'none'}),
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
  [Input(i, 'value') for i in INPUT_IDs] + [Input('camera-view-values', 'children')],
  [State('hexapod-plot', 'figure')]
)
def update_hexapod_plot(alpha, beta, gamma, f, s, m, h, k, a, camera, figure):
  if figure is None:
    return HEXAPOD_FIGURE

  virtual_hexapod = VirtualHexapod(
    h or 0, 
    k or 0, 
    a or 0, 
    f or 0, 
    m or 0, 
    s or 0)

  for leg in virtual_hexapod.legs:
    leg.change_pose(alpha, beta, gamma)
  
  if camera is not None:
    figure = BASE_PLOTTER.change_camera_view(figure, json.loads(camera))

  return BASE_PLOTTER.update(figure, virtual_hexapod)
