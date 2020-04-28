import dash_core_components as dcc
import dash_html_components as html
from hexapod.const import NAMES_LEG
from widgets.section_maker import make_section_type4
from widgets.pose_control.joint_widget_maker import (
    make_all_joint_widgets,
    make_slider,
)
from widgets.pose_control.components import HEADER


def make_leg_sections(jwidgets):
    widget_sections = []
    header_section = make_section_type4(
        "", html.H5("coxia"), html.H5("femur"), html.H5("tibia")
    )
    widget_sections.append(header_section)

    for leg in NAMES_LEG:
        header = html.Label(dcc.Markdown("**`{}`**".format(leg)))
        coxia = jwidgets[leg]["coxia"]
        femur = jwidgets[leg]["femur"]
        tibia = jwidgets[leg]["tibia"]
        section = make_section_type4(header, coxia, femur, tibia)
        widget_sections.append(section)

    return html.Div(widget_sections)


# ................................
# COMPONENTS
# ................................

widgets = make_all_joint_widgets(joint_input_function=make_slider)
sections = make_leg_sections(widgets)
KINEMATICS_WIDGETS_SECTION = html.Div([HEADER, sections])
