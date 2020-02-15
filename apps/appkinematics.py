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
  return dcc.Slider(id=name, min=-135, max=135, marks=slider_marks, value=0)

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
# PARTIALS
# -----------
def make_section_type4(div1, div2, div3, div4, name1='', name2='', name3='', name4=''):
  return html.Div([
    html.Div([html.Label(name1), div1], style={'width': '10%'}),
    html.Div([html.Label(name2), div2], style={'width': '30%'}),
    html.Div([html.Label(name3), div3], style={'width': '30%'}),
    html.Div([html.Label(name4), div4], style={'width': '30%'}),
    ],
    style={'display': 'flex'}
  )

def make_leg_sections():
  sections = []
  for leg in NAMES_LEG:
    header = html.Label(leg)
    coxia = SLIDERS[leg]['coxia']['slider']
    femur = SLIDERS[leg]['femur']['slider']
    tibia = SLIDERS[leg]['tibia']['slider']
    section = make_section_type4(header, coxia, femur, tibia)
    sections.append(section)

  return html.Div(sections)

SECTION_LEG_SLIDERS = make_leg_sections()

# hidden values of legs
SECTION_LEG_POSES = html.Div([html.Div(id='pose-{}'.format(leg_name), style={'display': 'none'}) for leg_name in NAMES_LEG])

# -----------
# LAYOUT
# -----------
layout = html.Div([
  SECTION_LEG_SLIDERS, 
  html.Div(id='display-pose'),
  SECTION_LEG_POSES  
])

# -----------
# CALLBACKS
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
  [Input('pose-{}'.format(leg), 'children') for leg in NAMES_LEG]
)
def display_pose(rm, rf, lf, lm, lb, rb):
  poses = [rm, rf, lf, lm, lb, rb]
  text = '\n'
  for leg_name, leg_pose in zip(NAMES_LEG, poses):
    leg = json.loads(leg_pose or '')
    header = '\n **{}** \n'.format(leg_name)
    coxia = ' - `coxia: {}`\n '.format(leg['coxia'])
    femur = ' - `femur: {}`\n '.format(leg['femur'])
    tibia = ' - `tibia: {}`\n '.format(leg['tibia'])
    text += (header + coxia + femur + tibia)

  return dcc.Markdown(text)