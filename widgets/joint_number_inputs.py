import dash_core_components as dcc
import dash_html_components as html
from .sectioning import make_section_type3, make_section_type4, make_section_type2
from hexapod.const import NAMES_JOINT, NAMES_LEG

def make_joint_number_input(_name):
  return dcc.Input(
    id=_name,
    type='number',
    value=0.0,
    step=5.0,
    min=-135.0,
    max=135.0,
    style={'marginRight': '5%', 'width': '95%', 'marginBottom': '5%'})

# input id format:
# 'input' + '-' + ['left', 'right'] + '-' + ['front', 'middle', 'back'] + '-' ['coxia', 'femur', 'tibia']
# input dictionary structure
# JOINT_INPUTS['left-front']['coxia'] =  INPUT_COMPONENT
# JOINT_INPUTS['right-middle']['femur'] = INPUT_COMPONENT
def make_joint_inputs():
  all_joint_inputs = {}

  for leg_name in NAMES_LEG:
    leg_joint_inputs = {}

    for joint_name in NAMES_JOINT:
      input_name = 'input-{}-{}'.format(leg_name, joint_name)
      leg_joint_inputs[joint_name] = make_joint_number_input(input_name)

    all_joint_inputs[leg_name] = leg_joint_inputs

  return all_joint_inputs

JOINT_INPUTS = make_joint_inputs()

def code(name):
  return dcc.Markdown('**`{}`**'.format(name))

def make_leg_section(name):
  coxia = JOINT_INPUTS[name]['coxia']
  femur = JOINT_INPUTS[name]['femur']
  tibia = JOINT_INPUTS[name]['tibia']

  return html.Div([
    html.H6(code('(' + name + ')')),
    make_section_type3(coxia, femur, tibia, code('coxia'), code('femur'), code('tibia'))
  ])

lf = make_leg_section('left-front')
rf = make_leg_section('right-front')
lm = make_leg_section('left-middle')
rm = make_leg_section('right-middle')
lb = make_leg_section('left-back')
rb = make_leg_section('right-back')

SECTION_POSE_CONTROL = html.Div([
  make_section_type2(lf, rf),
  make_section_type2(lm, rm),
  make_section_type2(lb, rb)
])