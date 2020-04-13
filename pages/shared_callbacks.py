from widgets.dimensions_ui import DIMENSION_INPUTS
import json
from app import app
from dash.dependencies import Output, Input
import dash_html_components as html

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
