# Widgets used to set the dimensions of the hexapod
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from texts import DIMENSIONS_WIDGETS_HEADER
from settings import INPUT_DIMENSIONS_RESOLUTION
from style_settings import NUMBER_INPUT_STYLE
from widgets.section_maker import make_section_type3


def make_number_widget(_name, _value):
    return dcc.Input(
        id=_name,
        type="number",
        value=_value,
        min=0,
        step=INPUT_DIMENSIONS_RESOLUTION,
        style=NUMBER_INPUT_STYLE,
    )


def _code(name):
    return dcc.Markdown(f"`{name}`")


# ................................
# COMPONENTS
# ................................

HEADER = html.Label(dcc.Markdown(f"**{DIMENSIONS_WIDGETS_HEADER}**"))
WIDGET_NAMES = ["front", "side", "middle", "coxia", "femur", "tibia"]
DIMENSION_WIDGET_IDS = [f"widget-dimension-{name}" for name in WIDGET_NAMES]
DIMENSION_CALLBACK_INPUTS = [Input(id, "value") for id in DIMENSION_WIDGET_IDS]

widgets = [make_number_widget(widget_id, 100) for widget_id in DIMENSION_WIDGET_IDS]
sections = [
    make_section_type3(
        widgets[0],
        widgets[1],
        widgets[2],
        _code(WIDGET_NAMES[0]),
        _code(WIDGET_NAMES[1]),
        _code(WIDGET_NAMES[2]),
    ),
    make_section_type3(
        widgets[3],
        widgets[4],
        widgets[5],
        _code(WIDGET_NAMES[3]),
        _code(WIDGET_NAMES[4]),
        _code(WIDGET_NAMES[5]),
    ),
]

DIMENSIONS_WIDGETS_SECTION = html.Div(
    [HEADER, html.Div(sections, style={"display": "flex"}), html.Br()]
)
