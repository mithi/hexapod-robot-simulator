import dash_core_components as dcc
import dash_html_components as html
from hexapod.const import NAMES_LEG
from widgets.sectioning import make_section_type3, make_section_type4, make_section_type2, make_section_type6
from widgets.joint_input_maker import make_all_joint_inputs, make_joint_knob_input

JOINT_INPUTS = make_all_joint_inputs(joint_input_function=make_joint_knob_input)

def make_leg_sections():
  row0 = []
  row1 = []
  row2 = []
  row3 = []
  for leg in NAMES_LEG:
    header = html.Label(dcc.Markdown(f'**{leg.upper()}**'))
    coxia = JOINT_INPUTS[leg]['coxia']
    femur = JOINT_INPUTS[leg]['femur']
    tibia = JOINT_INPUTS[leg]['tibia']

    row0.append(header)
    row1.append(coxia)
    row2.append(femur)
    row3.append(tibia)

  section0 = make_section_type6(row0[0], row0[1], row0[2], row0[3], row0[4], row0[5])
  section1 = make_section_type6(row1[0], row1[1], row1[2], row1[3], row1[4], row1[5])
  section2 = make_section_type6(row2[0], row2[1], row2[2], row2[3], row2[4], row2[5])
  section3 = make_section_type6(row3[0], row3[1], row3[2], row3[3], row3[4], row3[5])

  sections = [
    section1,
    section2,
    section3,
    section0,
  ]

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