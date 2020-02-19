import dash_core_components as dcc
import dash_html_components as html
from .sectioning import make_section_type3, make_section_type4, make_section_type2
from hexapod.const import NAMES_JOINT, NAMES_LEG

def make_joint_slider_input(name):
  slider_marks = {tick: str(tick) for tick in [-90, -45, 0, 45, 90]}
  return dcc.Slider(id=name, min=-105, max=105, marks=slider_marks, value=0, step=5)

# slider id format:
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
      leg_joint_inputs[joint_name] = make_joint_slider_input(input_name)

    all_joint_inputs[leg_name] = leg_joint_inputs

  return all_joint_inputs


JOINT_INPUTS = make_joint_inputs()

def make_leg_sections():
  sections = []
  header_section = make_section_type4('', html.H5('coxia'), html.H5('femur'), html.H5('tibia'))
  sections.append(header_section)

  for leg in NAMES_LEG:
    header = html.Label(dcc.Markdown('**`{}`**'.format(leg)))
    coxia = JOINT_INPUTS[leg]['coxia']
    femur = JOINT_INPUTS[leg]['femur']
    tibia = JOINT_INPUTS[leg]['tibia']
    section = make_section_type4(header, coxia, femur, tibia)
    sections.append(section)

  return html.Div(sections)

# -----------
# PARTIAL SECTIONS
# -----------
# section displaying all legs
SECTION_LEG_SLIDERS = make_leg_sections()

SECTION_POSE_CONTROL = html.Div([
  html.H4('Joint Angles (pose of each leg)'),
  SECTION_LEG_SLIDERS,
  html.Br()
])