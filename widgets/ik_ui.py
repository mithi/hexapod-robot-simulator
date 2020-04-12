# This module holds the widgets for the inverse kinematics page
from style_settings import SLIDER_THEME, SLIDER_HANDLE_COLOR, SLIDER_COLOR
from settings import (
    UPDATE_MODE,
    BODY_MAX_ANGLE,
    HIP_STANCE_MAX_ANGLE,
    LEG_STANCE_MAX_ANGLE,
)

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

HANDLE_STYLE = {
    "showCurrentValue": True,
    "color": SLIDER_HANDLE_COLOR,
}


def make_translate_slider(name, slider_label, type="translate_slider"):
    HANDLE_STYLE["label"] = slider_label
    return dash_daq.Slider(  # pylint: disable=not-callable
        id=name,
        min=-1.0,
        max=1.0,
        value=0.05,
        step=0.05,
        vertical=True,
        size=140,
        updatemode=UPDATE_MODE,
        handleLabel=HANDLE_STYLE,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )


def make_rotate_slider(
    name, slider_label, max_angle=BODY_MAX_ANGLE, size=140, vert=True
):
    HANDLE_STYLE["label"] = slider_label
    return dash_daq.Slider(  # pylint: disable=not-callable
        id=name,
        min=-max_angle,
        max=max_angle,
        value=1.5,
        step=1.5,
        vertical=vert,
        size=140,
        updatemode=UPDATE_MODE,
        handleLabel=HANDLE_STYLE,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
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

stance_style = {"padding": "3em 0 0.25em 2em"}
section_ik_start = html.Div(
    [html.Div(div_sh, style=stance_style), html.Div(div_sl, style=stance_style)],
    style={"display": "flex", "flex-direction": "row"},
)

divs = [div_ex, div_ey, div_ez, div_rx, div_ry, div_rz]
IK_SLIDERS_STYLE = {"padding": "0 0 0 4.0em"}
SLIDERS_LIST = [html.Div(div, style=IK_SLIDERS_STYLE) for div in divs]

section_ik_sliders = html.Div(
    SLIDERS_LIST, style={"display": "flex", "flex-direction": "row"},
)

SECTION_IK = html.Div(
    [
        html.Label(dcc.Markdown("**INVERSE KINEMATICS CONTROL**")),
        section_ik_sliders,
        section_ik_start,
    ]
)
