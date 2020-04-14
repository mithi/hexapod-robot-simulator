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

HEADER = html.Label(dcc.Markdown("**INVERSE KINEMATICS CONTROL**"))
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
    handle_style = {
        "showCurrentValue": True,
        "color": SLIDER_HANDLE_COLOR,
        "label": slider_label,
    }

    return dash_daq.Slider(  # pylint: disable=not-callable
        id=name,
        min=-1.0,
        max=1.0,
        value=0.05,
        step=0.05,
        vertical=True,
        size=90,
        updatemode=UPDATE_MODE,
        handleLabel=handle_style,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )


def make_rotate_slider(name, slider_label, max_angle=BODY_MAX_ANGLE, size=140):
    handle_style = {
        "showCurrentValue": True,
        "color": SLIDER_HANDLE_COLOR,
        "label": slider_label,
    }
    return dash_daq.Slider(  # pylint: disable=not-callable
        id=name,
        min=-max_angle,
        max=max_angle,
        value=1.5,
        step=1.5,
        vertical=True,
        size=90,
        updatemode=UPDATE_MODE,
        handleLabel=handle_style,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )


div_sh = make_rotate_slider(
    "input-start-hip-stance", "start \n hip.stance", HIP_STANCE_MAX_ANGLE
)
div_sl = make_rotate_slider(
    "input-start-leg-stance", "start \n leg.stance", LEG_STANCE_MAX_ANGLE
)

div_rx = make_rotate_slider("input-end-rot-x", "rot.x")
div_ry = make_rotate_slider("input-end-rot-y", "rot.y")
div_rz = make_rotate_slider("input-end-rot-z", "rot.z")

div_ex = make_translate_slider("input-end-percent-x", "percent.x")
div_ey = make_translate_slider("input-end-percent-y", "percent.y")
div_ez = make_translate_slider("input-end-percent-z", "percent.z")

ik_style = {"padding": "1.0em 0 0 4.0em"}
divs1 = [div_sh, div_ex, div_ey, div_ez]
divs2 = [div_sl, div_rx, div_ry, div_rz]
sliders_row1 = [html.Div(div, style=ik_style) for div in divs1]
sliders_row2 = [html.Div(div, style=ik_style) for div in divs2]

section_row1 = html.Div(sliders_row1, style={"display": "flex", "flex-direction": "row"},)

section_row2 = html.Div(sliders_row2, style={"display": "flex", "flex-direction": "row"},)

SECTION_IK = html.Div([HEADER, section_row1, section_row2])
