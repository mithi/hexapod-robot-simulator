import dash_core_components as dcc
import dash_html_components as html
from widgets.section_maker import make_section_type3, make_section_type2
from widgets.pose_control.components import HEADER


def make_section(joint_widgets, add_joint_names=False, style_to_use=None):
    names = [
        "left-front",
        "right-front",
        "left-middle",
        "right-middle",
        "left-back",
        "right-back",
    ]

    lf, rf, lm, rm, lb, rb = [
        make_leg_section(name, joint_widgets, add_joint_names) for name in names
    ]

    widget_sections = html.Div(
        [
            make_section_type2(lf, rf),
            make_section_type2(lm, rm),
            make_section_type2(lb, rb),
        ],
        style=style_to_use or {},
    )

    return html.Div([HEADER, widget_sections])


def code(name):
    return dcc.Markdown(f"`{name}`")


def make_leg_section(name, joint_widgets, add_joint_names=False):
    header = html.Label(dcc.Markdown(f"( `{name.upper()}` )"))
    coxia = joint_widgets[name]["coxia"]
    femur = joint_widgets[name]["femur"]
    tibia = joint_widgets[name]["tibia"]

    if add_joint_names:
        section = make_section_type3(
            coxia, femur, tibia, code("coxia"), code("femur"), code("tibia")
        )
    else:
        section = make_section_type3(coxia, femur, tibia)

    return html.Div([header, section])
