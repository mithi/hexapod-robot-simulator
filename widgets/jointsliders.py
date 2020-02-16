import dash_core_components as dcc
import dash_html_components as html
from .sectioning import make_section_type3, make_section_type4

NAMES_LEG = ['right-middle', 'right-front', 'left-front', 'left-middle', 'left-back', 'right-back']
NAMES_JOINT = ['coxia', 'femur', 'tibia']

# -----------
# SLIDERS FOR JOINTS
# -----------

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