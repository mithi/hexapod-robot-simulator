# Widgets used to control the dimensions of the hexapod
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from .sectioning import make_section_type3
from settings import DARKMODE

number_input_style={
    'marginRight': '5%',
    'width': '95%',
    'marginBottom': '5%',
    'borderRadius': '10px',
    'border': 'solid 1px',
    'fontFamily': "Courier New"
}

if DARKMODE:
    number_input_style['backgroundColor'] = '#2c3e50'
    number_input_style['color'] = '#FFFFFF'

INPUT_DIMENSIONS_IDs = [
    "input-length-front",
    "input-length-side",
    "input-length-middle",
    "input-length-coxia",
    "input-length-femur",
    "input-length-tibia",
]

DIMENSION_INPUTS = [Input(input_id, "value") for input_id in INPUT_DIMENSIONS_IDs]

def make_positive_number_input(_name, _value):
    return dcc.Input(
        id=_name, type="number", value=_value, step=5, min=0, style=number_input_style
    )


front_input = make_positive_number_input("input-length-front", 100)
side_input = make_positive_number_input("input-length-side", 100)
middle_input = make_positive_number_input("input-length-middle", 100)
coxia_input = make_positive_number_input("input-length-coxia", 100)
femur_input = make_positive_number_input("input-length-femur", 100)
tibia_input = make_positive_number_input("input-length-tibia", 100)

# -----------
# PARTIAL SECTIONS
# -----------
# section for hexapod measurement adjustments
sections = [
    make_section_type3(
        front_input, middle_input, side_input, "front", "middle", "side"
    ),
    make_section_type3(
        coxia_input, femur_input, tibia_input, "coxia", "femur", "tibia"
    ),
]

header = html.Label(dcc.Markdown("**HEXAPOD ROBOT DIMENSIONS**"))
SECTION_DIMENSION_CONTROL = html.Div(
    [header, html.Div(sections, style={"display": "flex"}), html.Br()]
)
