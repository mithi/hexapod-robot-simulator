import dash_core_components as dcc
import dash_html_components as html
from hexapod.const import NAMES_LEG
from widgets.sectioning import make_section_type3, make_section_type4, make_section_type2
from widgets.joint_input_maker import make_all_joint_inputs, make_joint_daq_slider_input

JOINT_INPUTS = make_all_joint_inputs(joint_input_function=make_joint_daq_slider_input)

def make_leg_sections():
  sections = [html.Br(), html.Br()]

  for leg in NAMES_LEG:
    header = html.Label(dcc.Markdown(f'**`{leg.upper()}`**'))
    coxia = JOINT_INPUTS[leg]['coxia']
    femur = JOINT_INPUTS[leg]['femur']
    tibia = JOINT_INPUTS[leg]['tibia']
    section = make_section_type4(header, coxia, femur, tibia)
    sections.append(section)
    sections.append(html.Br())

  return html.Div(sections)

# section displaying all legs
SECTION_LEG_SLIDERS = make_leg_sections()

SECTION_POSE_CONTROL = html.Div([
  SECTION_LEG_SLIDERS,
  html.Br()
])

SECTION_POSE_CONTROL_DAQ = html.Div([
  SECTION_LEG_SLIDERS,
  html.Br()
])