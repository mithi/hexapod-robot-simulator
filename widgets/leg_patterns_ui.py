# Widgets used to control the leg pose of all legs uniformly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
import dash_daq
from settings import ALPHA_MAX_ANGLE, BETA_MAX_ANGLE, GAMMA_MAX_ANGLE, UPDATE_MODE
from style_settings import SLIDER_THEME, SLIDER_HANDLE_COLOR, SLIDER_COLOR


LEG_SLIDERS_IDs = ["slider-alpha", "slider-beta", "slider-gamma"]
LEG_SLIDERS_INPUTS = [Input(i, "value") for i in LEG_SLIDERS_IDs]

HANDLE_STYLE = {
    "showCurrentValue": True,
    "color": SLIDER_HANDLE_COLOR,
}


def make_slider(name, max_angle):
    _, angle = name.split("-")
    HANDLE_STYLE["label"] = angle
    daq_slider = dash_daq.Slider(  # pylint: disable=not-callable
        id=name,
        min=-max_angle,
        max=max_angle,
        value=1.5,
        step=1.5,
        size=300,
        updatemode=UPDATE_MODE,
        handleLabel=HANDLE_STYLE,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )

    return html.Div(daq_slider, style={"padding": "2em"})


SLIDER_ALPHA = make_slider("slider-alpha", ALPHA_MAX_ANGLE)
SLIDER_BETA = make_slider("slider-beta", BETA_MAX_ANGLE)
SLIDER_GAMMA = make_slider("slider-gamma", GAMMA_MAX_ANGLE)
header = html.Label(dcc.Markdown("**LEG POSE CONTROL**"))
SECTION_LEG_POSE_SLIDERS = html.Div([header, SLIDER_ALPHA, SLIDER_BETA, SLIDER_GAMMA])
