import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from texts import KINEMATICS_WIDGETS_HEADER
from hexapod.const import NAMES_LEG, NAMES_JOINT


def make_joint_callback_inputs_of_one_leg(leg_name):
    return [
        Input(f"widget-{leg_name}-{joint_name}", "value") for joint_name in NAMES_JOINT
    ]


def make_all_joint_callback_inputs():
    callback_inputs = []
    for leg_name in NAMES_LEG:
        callback_inputs += make_joint_callback_inputs_of_one_leg(leg_name)
    return callback_inputs


# ................................
# COMPONENTS
# ................................

HEADER = html.Label(dcc.Markdown(f"**{KINEMATICS_WIDGETS_HEADER}**"))
KINEMATICS_CALLBACK_INPUTS = make_all_joint_callback_inputs()
