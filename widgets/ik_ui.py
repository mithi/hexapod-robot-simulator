# Widgets used to set the inverse kinematics parameters
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
import dash_daq
from texts import IK_WIDGETS_HEADER
from style_settings import (
    SLIDER_THEME,
    SLIDER_HANDLE_COLOR,
    SLIDER_COLOR,
    IK_SLIDER_SIZE,
)
from settings import (
    UPDATE_MODE,
    BODY_MAX_ANGLE,
    HIP_STANCE_MAX_ANGLE,
    LEG_STANCE_MAX_ANGLE,
    SLIDER_ANGLE_RESOLUTION,
)


def make_row(divs):
    widget_style = {"padding": "1.0em 0 0 4.0em"}
    row_style = {"display": "flex", "flex-direction": "row"}
    widgets = [html.Div(div, style=widget_style) for div in divs]
    return html.Div(widgets, style=row_style)


def make_translate_slider(name, slider_label):
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
        size=IK_SLIDER_SIZE,
        updatemode=UPDATE_MODE,
        handleLabel=handle_style,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )


def make_rotate_slider(name, slider_label, max_angle=BODY_MAX_ANGLE):
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
        step=SLIDER_ANGLE_RESOLUTION,
        vertical=True,
        size=IK_SLIDER_SIZE,
        updatemode=UPDATE_MODE,
        handleLabel=handle_style,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )


# ................................
# COMPONENTS
# ................................

HEADER = html.Label(dcc.Markdown(f"**{IK_WIDGETS_HEADER}**"))
IK_WIDGETS_IDS = [
    "widget-start-hip-stance",
    "widget-start-leg-stance",
    "widget-percent-x",
    "widget-percent-y",
    "widget-percent-z",
    "widget-rot-x",
    "widget-rot-y",
    "widget-rot-z",
]
IK_CALLBACK_INPUTS = [Input(input_id, "value") for input_id in IK_WIDGETS_IDS]

w_hips = make_rotate_slider(
    IK_WIDGETS_IDS[0], "start\nhip.stance", HIP_STANCE_MAX_ANGLE
)
w_legs = make_rotate_slider(
    IK_WIDGETS_IDS[1], "start\nleg.stance", LEG_STANCE_MAX_ANGLE
)

w_tx = make_translate_slider(IK_WIDGETS_IDS[2], "percent.x")
w_ty = make_translate_slider(IK_WIDGETS_IDS[3], "percent.y")
w_tz = make_translate_slider(IK_WIDGETS_IDS[4], "percent.z")

w_rx = make_rotate_slider(IK_WIDGETS_IDS[5], "rot.x")
w_ry = make_rotate_slider(IK_WIDGETS_IDS[6], "rot.y")
w_rz = make_rotate_slider(IK_WIDGETS_IDS[7], "rot.z")

row1 = make_row([w_hips, w_tx, w_ty, w_tz])
row2 = make_row([w_legs, w_rx, w_ry, w_rz])

IK_WIDGETS_SECTION = html.Div([HEADER, row1, row2])
