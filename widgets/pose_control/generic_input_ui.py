import dash_core_components as dcc
import dash_html_components as html
from widgets.sectioning import make_section_type3, make_section_type4, make_section_type2
from widgets.joint_input_maker import make_all_joint_inputs, make_joint_number_input

JOINT_INPUTS = make_all_joint_inputs(joint_input_function= make_joint_number_input)

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