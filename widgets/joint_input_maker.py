import dash_core_components as dcc
import dash_html_components as html
import dash_daq

from hexapod.const import NAMES_JOINT, NAMES_LEG

def make_joint_daq_slider_input(name):
  _, _, _, angle = name.split('-')

  return dash_daq.Slider( # pylint: disable=not-callable
    id=name,
    min=-105,
    max=105,
    value=10,
    size=150,
    handleLabel={"showCurrentValue": True,"label": angle},
    step=1,
  )

def make_joint_slider_input(name):
  slider_marks = {tick: str(tick) for tick in [-90, -45, 0, 45, 90]}
  return dcc.Slider(id=name, min=-105, max=105, marks=slider_marks, value=0, step=5)

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
def make_all_joint_inputs(joint_input_function):
  all_joint_inputs = {}

  for leg_name in NAMES_LEG:
    leg_joint_inputs = {}

    for joint_name in NAMES_JOINT:
      input_name = 'input-{}-{}'.format(leg_name, joint_name)
      leg_joint_inputs[joint_name] = joint_input_function(input_name)

    all_joint_inputs[leg_name] = leg_joint_inputs

  return all_joint_inputs
