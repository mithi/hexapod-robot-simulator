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


# widget id format:
# 'widget' + '-' +  leg_x + '-' +  leg_y + '-' leg_joint
# leg_x = ['left', 'right']
# leg_y = ['front', 'middle', 'back']
# leg_joint = ['coxia', 'femur', 'tibia']
# input dictionary structure
# all_joint_widgets['left-front']['coxia'] =  joint_widget
# all_joint_widgets['right-middle']['femur'] = joint_widget
def make_all_joint_widgets(joint_input_function):
    all_joint_widgets = {}

    for leg_name in NAMES_LEG:
        leg_joint_widget = {}

        for joint_name in NAMES_JOINT:
            widget_id = "widget-{}-{}".format(leg_name, joint_name)
            leg_joint_widget[joint_name] = joint_input_function(
                widget_id, max_angles[joint_name]
            )

        all_joint_widgets[leg_name] = leg_joint_widget

    return all_joint_widgets


def make_daq_slider(widget_id, max_angle):
    _, _, _, angle = widget_id.split("-")

    handle_style = {
        "showCurrentValue": True,
        "color": SLIDER_HANDLE_COLOR,
        "label": angle,
    }

    return dash_daq.Slider(  # pylint: disable=not-callable
        id=widget_id,
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


def make_slider(widget_id, max_angle):
    slider_marks = {tick: str(tick) for tick in [-45, 0, 45]}
    return dcc.Slider(
        id=widget_id, min=-max_angle, max=max_angle, marks=slider_marks, value=0, step=5
    )


def make_number_widget(widget_id, max_angle):
    return dcc.Input(
        id=widget_id,
        type="number",
        value=0.0,
        min=-max_angle,
        max=max_angle,
        style=NUMBER_INPUT_STYLE,
    )
