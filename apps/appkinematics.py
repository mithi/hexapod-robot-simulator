import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json

from app import app
from app import HEXAPOD_MEASUREMENTS

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

# Camera inputs
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

# Hexapod Inputs

HEXYLENGTH_INPUT_FRONT = make_number_input('hexapod-length-front', -0.05)
HEXYLENGTH_INPUT_SIDE = make_number_input('hexapod-length-side', 0.0)
HEXYLENGTH_INPUT_MIDDLE = make_number_input('hexapod-length-middle', -0.1)

HEXYLENGTH_INPUT_COXIA = make_number_input('hexapod-length-front', 0.35)
HEXYLENGTH_INPUT_FEMUR = make_number_input('hexapod-length-front', 0.7)
HEXYLENGTH_INPUT_TIBIA = make_number_input('hexapod-length-front', 0.5)

# -----------
# PARTIALS
# -----------
def make_section_type4(div1, div2, div3, div4, name1='', name2='', name3='', name4=''):
  return html.Div([
    html.Div([html.Label(name1), div1], style={'width': '13%'}),
    html.Div([html.Label(name2), div2], style={'width': '29%'}),
    html.Div([html.Label(name3), div3], style={'width': '29%'}),
    html.Div([html.Label(name4), div4], style={'width': '29%'}),
    ],
    style={'display': 'flex'}
  )

def make_leg_sections():
  sections = []
  header_section = make_section_type4('', html.H4('coxia'), html.H4('femur'), html.H4('tibia'))
  sections.append(header_section)

  for leg in NAMES_LEG:
    header = html.Label(dcc.Markdown('**`{}`**'.format(leg)))
    coxia = SLIDERS[leg]['coxia']['slider']
    femur = SLIDERS[leg]['femur']['slider']
    tibia = SLIDERS[leg]['tibia']['slider']
    section = make_section_type4(header, coxia, femur, tibia)
    sections.append(section)

  return html.Div(sections)

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


# -----------
# LAYOUT
# -----------
layout = html.Div([
  html.Div([
    html.Div(id='display-pose', style={'width': '45%'}),
    html.Div(SECTION_LEG_SLIDERS, style={'width': '55%'}),
    ], style={'display': 'flex'}
  ),
  html.H4('Camera View Adjustment Controls'),
  SECTION_INPUT_CAMVIEW,
  SECTION_LEG_POSES, 
  html.Div(id='camera-view-values', style={'display': 'none'})
])

# -----------
# CAMERA VIEW CALLBACK
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


# -----------
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

# All poses
@app.callback(
  Output('display-pose', 'children'),
  [Input('pose-{}'.format(leg), 'children') for leg in NAMES_LEG] + [Input('camera-view-values', 'children')]
)
def display_pose(rm, rf, lf, lm, lb, rb, camera_view):
  poses = [rm, rf, lf, lm, lb, rb]
  text = '\n'
  for leg_name, leg_pose in zip(NAMES_LEG, poses):
    try:
      leg = json.loads(leg_pose or '')
      header = '\n **{}** '.format(leg_name)
      coxia = ' `coxia: {}` '.format(leg['coxia'])
      femur = ' `femur: {}` '.format(leg['femur'])
      tibia = ' `tibia: {}` \n'.format(leg['tibia'])
      text += (header + coxia + femur + tibia)
    except:
      print("ERROR:", leg_name)

  return dcc.Markdown(text + str(camera_view))