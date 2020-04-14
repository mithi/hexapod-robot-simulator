from widgets.dimensions_ui import DIMENSION_INPUTS
import json
from app import app
import dash_core_components as dcc
from dash.dependencies import Output, Input
import dash_html_components as html
from settings import (
    UI_CONTROLS_WIDTH,
    UI_GRAPH_WIDTH,
    UI_GRAPH_HEIGHT,
)

def make_page_layout(graph_name, section_controls):
    layout = html.Div(
        [
            html.Div(section_controls, style={"width": UI_CONTROLS_WIDTH}),
            dcc.Graph(
                id=graph_name, style={"width": UI_GRAPH_WIDTH, "height": UI_GRAPH_HEIGHT},
            ),
        ],
        style={"display": "flex"},
    )
    return layout

# -------------------
# CALLBACK TO UPDATE HEXAPOD DIMENSIONS
# -------------------
ID_DIMENSIONS_SECTION = "hexapod-dimensions-values"
SECTION_HIDDEN_BODY_DIMENSIONS = html.Div(
    id=ID_DIMENSIONS_SECTION, style={"display": "none"}
)
INPUT_DIMENSIONS_JSON = Input(ID_DIMENSIONS_SECTION, "children")
OUTPUT_DIMENSIONS_JSON = Output(ID_DIMENSIONS_SECTION, "children")


@app.callback(OUTPUT_DIMENSIONS_JSON, DIMENSION_INPUTS)
def update_hexapod_dimensions_shared(front, side, middle, coxia, femur, tibia):
    dimensions = {
        "front": front or 0,
        "side": side or 0,
        "middle": middle or 0,
        "coxia": coxia or 0,
        "femur": femur or 0,
        "tibia": tibia or 0,
    }
    return json.dumps(dimensions)
