import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from widgets.sectioning import make_section_type3
from widgets.measurements import SECTION_LENGTHS_CONTROL, INPUT_LENGTHS_IDs
from widgets.camview import SECTION_INPUT_CAMVIEW, CAMVIEW_INPUT_IDs
from widgets.misc import SECTION_SLIDERS_TEST, SLIDERS_TEST_IDs

from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlot
from hexapod.const import BASE_PLOTTER, NAMES_LEG, BASE_HEXAPOD
from hexapod.const import HEXAPOD_FIGURE, HEXAPOD_POSE
from hexapod.const import PREDEFINED_POSES

from copy import deepcopy
import json
from app import app

# -----------
# LAYOUT
# -----------
radio_items_section = dcc.RadioItems(
  id='predefined-poses',
  options=[{'label': i, 'value': i} for i in PREDEFINED_POSES.keys()],
  value='none',
  labelStyle={'display': 'inline-block'}
)

section_hexapod = html.Div([
  html.Div(dcc.Graph(id='hexapod-plot'), style={'width': '50%'}),
  html.Div([SECTION_LENGTHS_CONTROL, SECTION_SLIDERS_TEST], style={'width': '40%'}),
  html.Div(id='display-variables', style={'width': '10%'})],
  style={'display': 'flex'}
)

layout = html.Div([
  section_hexapod,

  html.H4('Camera View Adjustment Controls'),
  html.P('IMPORTANT! Hover on any hexapod point/vertex to set current camera view as default'),
  SECTION_INPUT_CAMVIEW,
  html.Br(),
  html.H4('Predefined poses'),
  html.Label("IMPORTANT! When a predefined pose is selected, custom leg angles input (alpha/beta/gamma) would be ignored. Select NONE to enable custom poses."),
  radio_items_section,
  html.Br(),
  html.Div(id='camera-view-values', style={'display': 'none'}),
  html.Div(id='variables', style={'display': 'none'}),
])

# -----------
# CALLBACKS
# -----------
@app.callback(
  [Output(i, 'value') for i in CAMVIEW_INPUT_IDs],
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
  s = ''
  for k, v in p.items():
    s += '- `{}: {}` \n'.format(k, v)

  return dcc.Markdown(s)


@app.callback(
  Output('hexapod-plot', 'figure'),
  [Input(i, 'value') for i in INPUT_IDs] + [Input('camera-view-values', 'children')] + [Input('predefined-poses', 'value')],
  [State('hexapod-plot', 'figure')]
)
def update_hexapod_plot(alpha, beta, gamma, f, s, m, h, k, a, camera, predefined_pose, figure):

  if figure is None:
    HEXAPOD = deepcopy(BASE_HEXAPOD)
    HEXAPOD.update(HEXAPOD_POSE)
    return BASE_PLOTTER.update(HEXAPOD_FIGURE, HEXAPOD)

  if camera is not None:
    figure = BASE_PLOTTER.change_camera_view(figure, json.loads(camera))

  virtual_hexapod = VirtualHexapod().new(
    f or 0,
    m or 0,
    s or 0,
    h or 0,
    k or 0,
    a or 0
  )

  if predefined_pose != 'NONE':
    pose = PREDEFINED_POSES[predefined_pose]
    virtual_hexapod.update(pose)
    return BASE_PLOTTER.update(figure, virtual_hexapod)

  POSES = deepcopy(HEXAPOD_POSE)

  for k, _ in POSES.items():
    POSES[k] = {
      'id': k,
      'name': NAMES_LEG[k],
      'coxia': alpha,
      'femur': beta,
      'tibia': gamma,
    }

  virtual_hexapod.update(POSES)

  BASE_PLOTTER.update(figure, virtual_hexapod)
  return BASE_PLOTTER.update(figure, virtual_hexapod)
