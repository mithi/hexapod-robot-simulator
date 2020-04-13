import dash_core_components as dcc
import dash_html_components as html
from widgets.sectioning import make_section_type3, make_section_type2

HEADER = html.Label(dcc.Markdown("**KINEMATICS CONTROL**"))


def code(name):
    return dcc.Markdown(f"`{name}`")


def make_leg_section(name, joint_inputs, add_joint_names=False):
    header = html.Label(dcc.Markdown(f"( `{name.upper()}` )"))
    coxia = joint_inputs[name]["coxia"]
    femur = joint_inputs[name]["femur"]
    tibia = joint_inputs[name]["tibia"]

    if add_joint_names:
        section = make_section_type3(
            coxia, femur, tibia, code("coxia"), code("femur"), code("tibia")
        )
    else:
        section = make_section_type3(coxia, femur, tibia)

    return html.Div([header, section])


def make_section_pose_control(joint_inputs, add_joint_names=False, style_to_use={}):
    lf = make_leg_section("left-front", joint_inputs, add_joint_names)
    rf = make_leg_section("right-front", joint_inputs, add_joint_names)
    lm = make_leg_section("left-middle", joint_inputs, add_joint_names)
    rm = make_leg_section("right-middle", joint_inputs, add_joint_names)
    lb = make_leg_section("left-back", joint_inputs, add_joint_names)
    rb = make_leg_section("right-back", joint_inputs, add_joint_names)
    sliders = html.Div(
        [
            make_section_type2(lf, rf),
            make_section_type2(lm, rm),
            make_section_type2(lb, rb),
        ],
        style=style_to_use
    )

    return html.Div([HEADER, sliders])
