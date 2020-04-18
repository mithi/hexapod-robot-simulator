# Used to build the widgets for changing the joint angles
import dash_core_components as dcc
import dash_daq
from hexapod.const import NAMES_JOINT, NAMES_LEG
from settings import (
    ALPHA_MAX_ANGLE,
    BETA_MAX_ANGLE,
    GAMMA_MAX_ANGLE,
    UPDATE_MODE,
)
from style_settings import (
    NUMBER_INPUT_STYLE,
    SLIDER_THEME,
    SLIDER_HANDLE_COLOR,
    SLIDER_COLOR,
)

max_angles = {
    "coxia": ALPHA_MAX_ANGLE,
    "femur": BETA_MAX_ANGLE,
    "tibia": GAMMA_MAX_ANGLE,
}


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
            input_name = "input-{}-{}".format(leg_name, joint_name)
            leg_joint_inputs[joint_name] = joint_input_function(
                input_name, max_angles[joint_name]
            )

        all_joint_inputs[leg_name] = leg_joint_inputs

    return all_joint_inputs


def make_joint_daq_slider_input(name, max_angle):
    _, _, _, angle = name.split("-")

    handle_style = {
        "showCurrentValue": True,
        "color": SLIDER_HANDLE_COLOR,
        "label": angle,
    }

    return dash_daq.Slider(  # pylint: disable=not-callable
        id=name,
        min=-max_angle,
        max=max_angle,
        value=1.5,
        step=1.5,
        size=80,
        vertical=True,
        updatemode=UPDATE_MODE,
        handleLabel=handle_style,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )


def make_joint_slider_input(name, max_angle):
    slider_marks = {tick: str(tick) for tick in [-45, 0, 45]}
    return dcc.Slider(
        id=name, min=-max_angle, max=max_angle, marks=slider_marks, value=0, step=5
    )


def make_joint_number_input(name, max_angle):
    return dcc.Input(
        id=name,
        type="number",
        value=0.0,
        min=-max_angle,
        max=max_angle,
        style=NUMBER_INPUT_STYLE,
    )
