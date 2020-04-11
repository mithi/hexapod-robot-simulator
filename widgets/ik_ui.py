# This module holds the widgets for the inverse kinematics page
from settings import UPDATE_MODE
from settings import BODY_MAX_ANGLE, HIP_STANCE_MAX_ANGLE, LEG_STANCE_MAX_ANGLE

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
import dash_daq

IK_INPUT_IDs = [
    "input-start-hip-stance",
    "input-start-leg-stance",
    "input-end-percent-x",
    "input-end-percent-y",
    "input-end-percent-z",
    "input-end-rot-x",
    "input-end-rot-y",
    "input-end-rot-z",
]
IK_INPUTS = [Input(input_id, "value") for input_id in IK_INPUT_IDs]


def make_translate_slider(name, slider_label, type="translate_slider"):
    return dash_daq.Slider(  # pylint: disable=not-callable
        id=name,
        min=-1.0,
        max=1.0,
        value=0.05,
        size=140,
        updatemode=UPDATE_MODE,
        vertical=True,
        handleLabel={"showCurrentValue": True, "label": slider_label},
        step=0.05,
    )


def make_rotate_slider(
    name, slider_label, max_angle=BODY_MAX_ANGLE, size=140, vert=True
):
    return dash_daq.Slider(  # pylint: disable=not-callable
        id=name,
        min=-max_angle,
        max=max_angle,
        value=1.5,
        size=size,
        updatemode=UPDATE_MODE,
        vertical=vert,
        handleLabel={"showCurrentValue": True, "label": slider_label},
        step=1.5,
    )


div_rx = make_rotate_slider("input-end-rot-x", "rot.x")
div_ry = make_rotate_slider("input-end-rot-y", "rot.y")
div_rz = make_rotate_slider("input-end-rot-z", "rot.z")
div_sh = make_rotate_slider(
    "input-start-hip-stance", "start.hip.stance", HIP_STANCE_MAX_ANGLE, 140, False
)
div_sl = make_rotate_slider(
    "input-start-leg-stance", "start.leg.stance", LEG_STANCE_MAX_ANGLE, 140, False
)
div_ex = make_translate_slider("input-end-percent-x", "percent.x")
div_ey = make_translate_slider("input-end-percent-y", "percent.y")
div_ez = make_translate_slider("input-end-percent-z", "percent.z")

section_ik_start = html.Div(
    [
        html.Div(div_sh, style={"padding": "3em 0 0.25em 2em"}),
        html.Div(div_sl, style={"padding": "3em 0 0.25em 2em"}),
    ],
    style={"display": "flex", "flex-direction": "row"},
)

section_ik_sliders = html.Div(
    [
        html.Div(div_ex, style={"padding": "0 0 0 3.5em"}),
        html.Div(div_ey, style={"padding": "0 0 0 3.5em"}),
        html.Div(div_ez, style={"padding": "0 0 0 3.5em"}),
        html.Div(div_rx, style={"padding": "0 0 0 3.5em"}),
        html.Div(div_ry, style={"padding": "0 0 0 3.5em"}),
        html.Div(div_rz, style={"padding": "0 0 0 3.5em"}),
    ],
    style={"display": "flex", "flex-direction": "row"},
)

SECTION_IK = html.Div(
    [
        html.Label(dcc.Markdown("**INVERSE KINEMATICS CONTROL**")),
        section_ik_sliders,
        section_ik_start,
    ]
)
