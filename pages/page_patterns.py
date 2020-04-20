import json
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, BASE_FIGURE
from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL
from widgets.leg_patterns_ui import SECTION_LEG_POSE_SLIDERS, LEG_SLIDERS_INPUTS
from pages import helpers
from pages.shared import (
    INPUT_DIMENSIONS_JSON,
    SECTION_HIDDEN_BODY_DIMENSIONS,
    make_page_layout,
)

# *********************
# *  LAYOUT           *
# *********************
GRAPH_NAME = "graph-hexapod-patterns"
ID_MESSAGE_DISPLAY_SECTION = "display-message-patterns"
SECTION_MESSAGE_DISPLAY = html.Div(id=ID_MESSAGE_DISPLAY_SECTION)
ID_POSES_SECTION = "hexapod-poses-values-patterns"
SECTION_HIDDEN_JOINT_POSES = html.Div(id=ID_POSES_SECTION, style={"display": "none"})

SECTION_CONTROLS = [
    SECTION_DIMENSION_CONTROL,
    SECTION_LEG_POSE_SLIDERS,
    SECTION_MESSAGE_DISPLAY,
    SECTION_HIDDEN_BODY_DIMENSIONS,
    SECTION_HIDDEN_JOINT_POSES,
]

layout = make_page_layout(GRAPH_NAME, SECTION_CONTROLS)

# *********************
# *  CALLBACKS        *
# *********************

# ......................
# Update page
# ......................
OUTPUT_MESSAGE_DISPLAY = Output(ID_MESSAGE_DISPLAY_SECTION, "children")
INPUT_POSES_JSON = Input(ID_POSES_SECTION, "children")
OUTPUTS = [Output(GRAPH_NAME, "figure"), OUTPUT_MESSAGE_DISPLAY]
INPUTS = [INPUT_DIMENSIONS_JSON, INPUT_POSES_JSON]
STATES = [State(GRAPH_NAME, "relayoutData"), State(GRAPH_NAME, "figure")]


@app.callback(OUTPUTS, INPUTS, STATES)
def update_patterns_page(dimensions_json, poses_json, relayout_data, figure):
    if figure is None:
        return BASE_FIGURE, ""

    dimensions = helpers.load_dimensions(dimensions_json)
    poses = json.loads(poses_json)
    hexapod = VirtualHexapod(dimensions)

    try:
        hexapod.update(poses)
    except Exception as alert:
        return figure, helpers.make_alert_message(alert)

    BASE_PLOTTER.update(figure, hexapod)
    helpers.change_camera_view(figure, relayout_data)
    return figure, ""


OUTPUT = Output(ID_POSES_SECTION, "children")
INPUTS = LEG_SLIDERS_INPUTS

# ......................
# Update parameters
# ......................
@app.callback(OUTPUT, INPUTS)
def update_poses_alpha_beta_gamma(alpha, beta, gamma):
    return json.dumps(helpers.make_pose(alpha, beta, gamma))
