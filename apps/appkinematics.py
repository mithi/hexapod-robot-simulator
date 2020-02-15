import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json

from app import app
from app import HEXAPOD_MEASUREMENTS

from hexapod import Point, Linkage, Hexagon, VirtualHexapod, HexapodPlot

# -----------
# SLIDERS FOR JOINTS
# -----------
NAMES_LEG = ['right-middle', 'right-front', 'left-front', 'left-middle', 'left-back', 'right-back']
NAMES_JOINT = ['coxia', 'femur', 'tibia']

def make_slider(name):
  slider_marks = {tick: str(tick) for tick in [-90, -45, 0, 45, 90]}
  return dcc.Slider(id=name, min=-105, max=105, marks=slider_marks, value=0, step=5)

# EXAMPLE:
# SLIDERS['left-front'] = {'coxia' : {'slider': SLIDER, 'id': 'slider-left-front-coxia'}}
# SLIDERS['right-middle'] = {'femur' : {'slider': SLIDER, 'id': 'slider-right-middle-femur'}}
def make_sliders():
  sliders_leg = {}

  for leg_name in NAMES_LEG:
    sliders_joint = {}
    
    for joint_name in NAMES_JOINT:
      slider_name = 'slider-' + leg_name + '-' + joint_name
      slider = make_slider(slider_name)
      sliders_joint[joint_name] = { 'slider': slider, 'id': slider_name }
    
    sliders_leg[leg_name] = sliders_joint

  return sliders_leg

# format:
# 'slider' + '-' + ['left', 'right'] + '-' + ['front', 'middle', 'back'] + '-' ['coxia', 'femur', 'tibia']
SLIDERS = make_sliders()

# -----------
# NUMBER INPUTS
# -----------

def make_number_input(_name, _value):
  return dcc.Input(id=_name, type='number', value=_value, step=0.005, style={'marginRight': '5%', 'width': '95%', 'marginBottom': '5%'})

def make_positive_number_input(_name, _value):
  return dcc.Input(id=_name, type='number', value=_value, step=5, min=0, style={'marginRight': '5%', 'width': '95%', 'marginBottom': '5%'})

# Camera view adjustment inputs
INPUT_CAMVIEW = {
  'up-x': make_number_input('input-view-up-x', 0.0),
  'up-y': make_number_input('input-view-up-y', 0.0),
  'up-z': make_number_input('input-view-up-z', 1.0),

  'center-x': make_number_input('input-view-center-x', -0.05),
  'center-y': make_number_input('input-view-center-y', 0.0),
  'center-z': make_number_input('input-view-center-z', -0.1),

  'eye-x': make_number_input('input-view-eye-x', 0.35),
  'eye-y': make_number_input('input-view-eye-y', 0.7),
  'eye-z': make_number_input('input-view-eye-z', 0.5),
}

# Hexapod measured lengths inputs
INPUT_LENGTHS = { 
  'front': make_positive_number_input('input-length-front', 100),
  'side': make_positive_number_input('input-length-side', 100),
  'middle': make_positive_number_input('input-length-middle', 100),
  'coxia': make_positive_number_input('input-length-coxia', 100),
  'femur': make_positive_number_input('input-length-femur', 100),
  'tibia': make_positive_number_input('input-length-tibia', 100),
}

# -----------
# HELPERS TO MAKE PARTIAL SECTIONS
# -----------
def make_section_type3(div1, div2, div3, div4, name1='', name2='', name3='', name4=''):
  return html.Div([
    html.Div([html.Label(name1), div1], style={'width': '33%'}),
    html.Div([html.Label(name2), div2], style={'width': '33%'}),
    html.Div([html.Label(name3), div3], style={'width': '33%'}),
    ],
    style={'display': 'flex'}
  )

def make_section_type4(div1, div2, div3, div4):
  return html.Div([
    html.Div(div1, style={'width': '13%'}),
    html.Div(div2, style={'width': '29%'}),
    html.Div(div3, style={'width': '29%'}),
    html.Div(div4, style={'width': '29%'}),
    ],
    style={'display': 'flex'}
  )

def make_leg_sections():
  sections = []
  header_section = make_section_type4('', html.H5('coxia'), html.H5('femur'), html.H5('tibia'))
  sections.append(header_section)

  for leg in NAMES_LEG:
    header = html.Label(dcc.Markdown('**`{}`**'.format(leg)))
    coxia = SLIDERS[leg]['coxia']['slider']
    femur = SLIDERS[leg]['femur']['slider']
    tibia = SLIDERS[leg]['tibia']['slider']
    section = make_section_type4(header, coxia, femur, tibia)
    sections.append(section)

  return html.Div(sections)

# -----------
# PARTIAL SECTIONS
# -----------
# section displaying all legs
SECTION_LEG_SLIDERS = make_leg_sections()

# hidden values of legs
SECTION_LEG_POSES = html.Div([html.Div(id='pose-{}'.format(leg_name), style={'display': 'none'}) for leg_name in NAMES_LEG])

# section for camera view adjustments
section_input_up = make_section_type4(dcc.Markdown('`(UP)`'), INPUT_CAMVIEW['up-x'], INPUT_CAMVIEW['up-y'], INPUT_CAMVIEW['up-z'])
section_input_center = make_section_type4(dcc.Markdown('`(CNTR)`'), INPUT_CAMVIEW['center-x'], INPUT_CAMVIEW['center-y'], INPUT_CAMVIEW['center-z'])
section_input_eye = make_section_type4(dcc.Markdown('`(EYE)`'), INPUT_CAMVIEW['eye-x'], INPUT_CAMVIEW['eye-y'], INPUT_CAMVIEW['eye-z'])
SECTION_INPUT_CAMVIEW = html.Div([
  html.Div(section_input_up, style={'width': '33%'}),
  html.Div(section_input_center, style={'width': '33%'}),
  html.Div(section_input_eye, style={'width': '33%'}),
  ],
  style={'display': 'flex'}
)

html.Div([section_input_up, section_input_center, section_input_eye])

# section for hexapod measurement adjustments
section_input_body = make_section_type3(INPUT_LENGTHS['front'], INPUT_LENGTHS['middle'], INPUT_LENGTHS['side'], '', 'front', 'middle', 'side')
section_input_leg = make_section_type3(INPUT_LENGTHS['coxia'], INPUT_LENGTHS['femur'], INPUT_LENGTHS['tibia'], '', 'coxia', 'femur', 'tibia')

SECTION_INPUT_LENGTHS = html.Div([
  html.Div(section_input_body, style={'width':  '50%'}),
  html.Div(section_input_leg, style={'width': '50%'}),
  ],
  style={'display': 'flex'}
)

# -----------
# LAYOUT
# -----------
layout = html.Div([
  html.Div([
    dcc.Graph(id='graph-hexapod', style={'width': '45%'}),

    html.Div([
      html.H4('Joint Angles (Pose of each Leg)'),
      SECTION_LEG_SLIDERS,
      html.Br(),
      html.H4('Hexapod Robot Measurements'),
      SECTION_INPUT_LENGTHS  
      ], style={'width': '55%'}),
    ], style={'display': 'flex'}
  ),

  html.H4('Camera View Adjustment Controls'),
  SECTION_INPUT_CAMVIEW,
  html.Br(),

  # HIDDEN SECTIONS
  SECTION_LEG_POSES, 
  html.Div(id='hexapod-measurements-values', style={'display': 'none'}),
  html.Div(id='camera-view-values', style={'display': 'none'})
])

# -----------
# Hexapod Measurements CALLBACK
# -----------
INPUT_LENGTHS_IDs = [
  'input-length-front',
  'input-length-side',
  'input-length-middle',

  'input-length-coxia',
  'input-length-femur',
  'input-length-tibia',
]
@app.callback(
  Output('hexapod-measurements-values', 'children'),
  [Input(input_id, 'value') for input_id in INPUT_LENGTHS_IDs]
)
def update_hexapod_measurements(fro, sid, mid, cox, fem, tib):
  measurements = {
    'front': fro or 0,
    'side': sid or 0,
    'middle': mid or 0,

    'coxia': cox or 0,
    'femur': fem or 0,
    'tibia': tib or 0, 
  }

  return json.dumps(measurements)

# -----------
# CameraCALLBACK
# -----------
INPUT_IDs = [
  'input-view-up-x',
  'input-view-up-y',
  'input-view-up-z',

  'input-view-center-x',
  'input-view-center-y',
  'input-view-center-z',

  'input-view-eye-x',
  'input-view-eye-y',
  'input-view-eye-z',
]
@app.callback(
  Output('camera-view-values', 'children'),
  [Input(input_id, 'value') for input_id in INPUT_IDs]
)
def update_camera_view(up_x, up_y, up_z, center_x, center_y, center_z, eye_x, eye_y, eye_z):
  
  camera = {
    'up': {'x': up_x or 0, 'y': up_y or 0, 'z': up_z or 0},
    'center': {'x': center_x or 0, 'y': center_y or 0, 'z': center_z or 0},
    'eye': {'x': (eye_x or 0), 'y': (eye_y or 0), 'z': (eye_z or 0)}
  }

  return json.dumps(camera)
# -------
# LEG CALLBACKS
# -----------
# front          x2          x1
#                 \         /
#                  *---*---*
#                 /    |    \
#                /     |     \
#               /      |      \
# middle  x3 --*------cog------*-- x0
#               \      |      /
#                \     |     /
#                 \    |    /
# back             *---*---*
#                 /         \
#                x4         x5
#               left       right

# 0
@app.callback(
  Output('pose-right-middle', 'children'),
  [Input('slider-right-middle-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_right_middle(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 1
@app.callback(
  Output('pose-right-front', 'children'),
  [Input('slider-right-front-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_right_front(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 2
@app.callback(
  Output('pose-left-front', 'children'),
  [Input('slider-left-front-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_left_front(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 3
@app.callback(
  Output('pose-left-middle', 'children'),
  [Input('slider-left-middle-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_left_middle(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 4
@app.callback(
  Output('pose-left-back', 'children'),
  [Input('slider-left-back-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_left_back(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# 5
@app.callback(
  Output('pose-right-back', 'children'),
  [Input('slider-right-back-{}'.format(joint), 'value') for joint in NAMES_JOINT]
)
def update_right_back(coxia, femur, tibia):
  return json.dumps({'coxia': coxia, 'femur': femur, 'tibia': tibia})

# -------
# FIGURE/GRAPH CALLBACK
# -----------
INPUT_ALL = [Input('pose-{}'.format(leg), 'children') for leg in NAMES_LEG] + \
  [Input(name, 'children') for name in ['camera-view-values', 'hexapod-measurements-values']]
@app.callback(
  Output('graph-hexapod', 'figure'),
  INPUT_ALL
)
def update_graph(rm, rf, lf, lm, lb, rb, cam_view, measurements):

  measurements = json.loads(measurements)
  cam_view = json.loads(cam_view)

  f, s, m = measurements['front'], measurements['side'], measurements['middle'],
  h, k, a = measurements['coxia'], measurements['femur'], measurements['tibia'],

  virtual_hexapod = VirtualHexapod(h, k, a, f, m, s)
  hexaplot = HexapodPlot(virtual_hexapod)
  
  poses = [rm, rf, lf, lm, lb, rb]
  for leg, pose in zip(virtual_hexapod.legs, poses):
    try:
      pose = json.loads(pose)
      alpha, beta, gamma = pose['coxia'], pose['femur'], pose['tibia']
      leg.change_pose(alpha, beta, gamma)
    except:
      print(pose)
      
  hexaplot.change_camera_view(cam_view)
  fig = hexaplot.update(virtual_hexapod)

  return fig