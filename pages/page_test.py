import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL, DIMENSION_INPUTS
from widgets.camview_ui import SECTION_INPUT_CAMVIEW, CAMVIEW_INPUTS, CAMVIEW_OUTPUTS
from widgets.alpha_beta_gamma_ui import SECTION_SLIDERS_TEST, SLIDERS_TEST_INPUTS
from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import (
  BASE_PLOTTER,
  NAMES_LEG, BASE_HEXAPOD,
  HEXAPOD_FIGURE,
  HEXAPOD_POSE
)

from copy import deepcopy
import json
from app import app

# -----------
# LAYOUT
# -----------
section_hexapod = html.Div([
  html.Div([
    html.H3(dcc.Markdown('**CUSTOM CONTROLS**')),
    SECTION_SLIDERS_TEST,
    html.Br(),
    SECTION_DIMENSION_CONTROL,
  ],
    style={'width': '40%'}
  ),
  html.Div(dcc.Graph(id='hexapod-plot'), style={'width': '50%'}),
  html.Div(id='display-variables', style={'width': '10%'}),
  ],
  style={'display': 'flex'}
)

layout = html.Div([
  section_hexapod,
  SECTION_INPUT_CAMVIEW,
  html.Div(id='camera-view-values', style={'display': 'none'}),
  html.Div(id='variables', style={'display': 'none'}),
])


# -----------
# CALLBACKS
# -----------
INPUTS = SLIDERS_TEST_INPUTS + DIMENSION_INPUTS + [Input('camera-view-values', 'children')]
@app.callback(
  Output('hexapod-plot', 'figure'),
  INPUTS,
  [State('hexapod-plot', 'figure')]
)
def update_hexapod_plot(alpha, beta, gamma, f, s, m, h, k, a, camera, figure):

  if figure is None:
    #print('No existing hexapod figure.')
    HEXAPOD = deepcopy(BASE_HEXAPOD)
    HEXAPOD.update(HEXAPOD_POSE)
    return BASE_PLOTTER.update(HEXAPOD_FIGURE, HEXAPOD)

  if camera is not None:
    #print('Camera view changed.')
    figure = BASE_PLOTTER.change_camera_view(figure, json.loads(camera))

  # Create a hexapod
  virtual_hexapod = VirtualHexapod().new(
    f or 0,
    m or 0,
    s or 0,
    h or 0,
    k or 0,
    a or 0
  )

  # Update Hexapod's pose given alpha, beta, and gamma
  poses = deepcopy(HEXAPOD_POSE)

  for k, _ in poses.items():
    poses[k] = {
      'id': k,
      'name': NAMES_LEG[k],
      'coxia': alpha,
      'femur': beta,
      'tibia': gamma,
    }

  virtual_hexapod.update(poses)

  # Update figure of hexapod and return it
  BASE_PLOTTER.update(figure, virtual_hexapod)
  return BASE_PLOTTER.update(figure, virtual_hexapod)


@app.callback(
  CAMVIEW_OUTPUTS,
  [Input('hexapod-plot', 'hoverData')],
  [State('hexapod-plot', 'relayoutData')]
)
def update_camera_inputs(hover_data, relayout_data):
  # We're only using the hover_data to trigger events
  # Using relayout_data to trigger events, causes the program
  # to crash (too many callbacks at a short period of time)

  if relayout_data is None:
    raise PreventUpdate

  if 'scene.camera' not in relayout_data:
    raise PreventUpdate

  camera = relayout_data['scene.camera']

  up = camera['up']
  c = camera['center']
  eye =  camera['eye']

  ux, uy, uz = up['x'], up['y'], up['z']
  cx, cy, cz = c['x'], c['y'], c['z']
  ex, ey, ez = eye['x'], eye['y'], eye['z']

  return ux, uy, uz, cx, cy, cz, ex, ey, ez


@app.callback(
  Output('camera-view-values', 'children'),
  CAMVIEW_INPUTS
)
def update_camera_view(up_x, up_y, up_z, center_x, center_y, center_z, eye_x, eye_y, eye_z):

  camera = {
    'up': {'x': up_x or 0, 'y': up_y or 0, 'z': up_z or 0},
    'center': {'x': center_x or 0, 'y': center_y or 0, 'z': center_z or 0},
    'eye': {'x': (eye_x or 0), 'y': (eye_y or 0), 'z': (eye_z or 0)}
  }

  return json.dumps(camera)


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
  s = ''
  for k, v in p.items():
    s += '- `{}: {}` \n'.format(k, v)

  return dcc.Markdown(s)
