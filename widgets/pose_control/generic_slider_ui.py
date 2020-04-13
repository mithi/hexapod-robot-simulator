import dash_core_components as dcc
import dash_html_components as html
from hexapod.const import NAMES_LEG
from widgets.sectioning import make_section_type4

from widgets.pose_control.joint_input_maker import (
    make_all_joint_inputs,
    make_joint_slider_input,
)

HEADER = html.Label(dcc.Markdown("**KINEMATICS CONTROL**"))
JOINT_INPUTS = make_all_joint_inputs(joint_input_function=make_joint_slider_input)


def make_leg_sections():
    sections = []
    header_section = make_section_type4(
        "", html.H5("coxia"), html.H5("femur"), html.H5("tibia")
    )
    sections.append(header_section)

    for leg in NAMES_LEG:
        header = html.Label(dcc.Markdown("**`{}`**".format(leg)))
        coxia = JOINT_INPUTS[leg]["coxia"]
        femur = JOINT_INPUTS[leg]["femur"]
        tibia = JOINT_INPUTS[leg]["tibia"]
        section = make_section_type4(header, coxia, femur, tibia)
        sections.append(section)

    return html.Div(sections)


section_leg_sliders = make_leg_sections()
SECTION_POSE_CONTROL = html.Div([HEADER, section_leg_sliders])
