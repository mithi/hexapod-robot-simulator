# Widgets used to control the leg pose of all legs uniformly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
import dash_daq
from settings import ALPHA_MAX_ANGLE, BETA_MAX_ANGLE, GAMMA_MAX_ANGLE
from settings import UPDATE_MODE
from .sectioning import make_section_type3

SLIDERS_TEST_IDs = ["slider-alpha", "slider-beta", "slider-gamma"]
SLIDERS_TEST_INPUTS = [Input(i, "value") for i in SLIDERS_TEST_IDs]


def make_slider(name, max_angle):
    _, angle = name.split("-")
    handle_label_items = {"showCurrentValue": True, "label": angle}
    daq_slider = dash_daq.Slider(  # pylint: disable=not-callable
        id=name,
        min=-max_angle,
        max=max_angle,
        value=1.5,
        size=300,
        step=1.5,
        vertical=True,
        updatemode=UPDATE_MODE,
        handleLabel=handle_label_items,
    )

    return html.Div(daq_slider, style={"padding": "0 0 0 3.5em"})


SLIDER_ALPHA = make_slider("slider-alpha", ALPHA_MAX_ANGLE)
SLIDER_BETA = make_slider("slider-beta", BETA_MAX_ANGLE)
SLIDER_GAMMA = make_slider("slider-gamma", GAMMA_MAX_ANGLE)
header = html.Label(dcc.Markdown("**LEG POSE CONTROL**"))
SECTION_SLIDERS_TEST = html.Div(
    [header, make_section_type3(SLIDER_ALPHA, SLIDER_BETA, SLIDER_GAMMA)]
)
