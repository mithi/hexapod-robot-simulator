# Widgets used to set the leg pose of all legs uniformly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
import dash_daq
from texts import PATTERNS_WIDGETS_HEADER
from settings import (
    ALPHA_MAX_ANGLE,
    BETA_MAX_ANGLE,
    GAMMA_MAX_ANGLE,
    UPDATE_MODE,
    SLIDER_ANGLE_RESOLUTION,
)
from style_settings import SLIDER_THEME, SLIDER_HANDLE_COLOR, SLIDER_COLOR


def make_slider(slider_id, name, max_angle):

    handle_style = {
        "showCurrentValue": True,
        "color": SLIDER_HANDLE_COLOR,
        "label": name,
    }

    daq_slider = dash_daq.Slider(  # pylint: disable=not-callable
        id=slider_id,
        min=-max_angle,
        max=max_angle,
        value=1.5,
        step=SLIDER_ANGLE_RESOLUTION,
        size=300,
        updatemode=UPDATE_MODE,
        handleLabel=handle_style,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )

    return html.Div(daq_slider, style={"padding": "2em"})


# ................................
# COMPONENTS
# ................................

HEADER = html.Label(dcc.Markdown(f"**{PATTERNS_WIDGETS_HEADER}**"))
WIDGET_NAMES = ["alpha", "beta", "gamma"]
PATTERNS_WIDGET_IDS = [f"widget-{name}" for name in WIDGET_NAMES]
PATTERNS_CALLBACK_INPUTS = [Input(i, "value") for i in PATTERNS_WIDGET_IDS]

max_angles = [ALPHA_MAX_ANGLE, BETA_MAX_ANGLE, GAMMA_MAX_ANGLE]
widgets = [
    make_slider(id, name, angle)
    for id, name, angle in zip(PATTERNS_WIDGET_IDS, WIDGET_NAMES, max_angles)
]
PATTERNS_WIDGETS_SECTION = html.Div([HEADER] + widgets)
