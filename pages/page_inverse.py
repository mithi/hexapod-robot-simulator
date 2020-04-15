from settings import RECOMPUTE_HEXAPOD
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, BASE_FIGURE
from hexapod.ik_solver.ik_solver import inverse_kinematics_update
from hexapod.ik_solver.recompute_hexapod import recompute_hexapod
from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL
from widgets.ik_ui import SECTION_IK, IK_INPUTS
from pages import helpers
from pages.shared import (
    INPUT_DIMENSIONS_JSON,
    SECTION_HIDDEN_BODY_DIMENSIONS,
    make_page_layout,
)
import json
from app import app
import dash_html_components as html
from dash.dependencies import Input, Output, State

# *********************
# *  LAYOUT           *
# *********************
GRAPH_NAME = "graph-hexapod-inverse"
ID_MESSAGE_DISPLAY_SECTION = "display-message-inverse"
SECTION_MESSAGE_DISPLAY = html.Div(id=ID_MESSAGE_DISPLAY_SECTION)
ID_IK_PARAMETERS_JSON = "ik-parameters"
SECTION_HIDDEN_IK_PARAMETERS = html.Div(
    id=ID_IK_PARAMETERS_JSON, style={"display": "none"}
)

SECTION_CONTROLS = [
    SECTION_DIMENSION_CONTROL,
    SECTION_IK,
    SECTION_MESSAGE_DISPLAY,
    SECTION_HIDDEN_BODY_DIMENSIONS,
    SECTION_HIDDEN_IK_PARAMETERS,
]

layout = make_page_layout(GRAPH_NAME, SECTION_CONTROLS)

# *********************
# *  CALLBACKS        *
# *********************

# ......................
# Update page
# ......................
OUTPUT_MESSAGE_DISPLAY = Output(ID_MESSAGE_DISPLAY_SECTION, "children")
OUTPUTS = [
    Output(GRAPH_NAME, "figure"),
    OUTPUT_MESSAGE_DISPLAY,
]
INPUTS = [INPUT_DIMENSIONS_JSON, Input(ID_IK_PARAMETERS_JSON, "children")]
STATES = [State(GRAPH_NAME, "relayoutData"), State(GRAPH_NAME, "figure")]


@app.callback(OUTPUTS, INPUTS, STATES)
def update_inverse_page(dimensions_json, ik_parameters_json, relayout_data, figure):
    if figure is None:
        return BASE_FIGURE, ""

    dimensions = helpers.load_dimensions(dimensions_json)
    ik_parameters = json.loads(ik_parameters_json)
    hexapod = VirtualHexapod(dimensions)

    try:
        poses, hexapod = inverse_kinematics_update(hexapod, ik_parameters)
    except Exception as alert:
        return figure, helpers.make_alert_message(str(alert))

    if RECOMPUTE_HEXAPOD:
        try:
            hexapod = recompute_hexapod(dimensions, ik_parameters, poses)
        except Exception as alert:
            return figure, helpers.make_alert_message(str(alert))

    BASE_PLOTTER.update(figure, hexapod)
    helpers.change_camera_view(figure, relayout_data)
    return figure, helpers.make_poses_message(poses)


# ......................
# Update parameters
# ......................
OUTPUT = Output(ID_IK_PARAMETERS_JSON, "children")


@app.callback(OUTPUT, IK_INPUTS)
def update_ik_parameters(
    hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z
):

    return json.dumps(
        {
            "hip_stance": hip_stance,
            "leg_stance": leg_stance,
            "percent_x": percent_x,
            "percent_y": percent_y,
            "percent_z": percent_z,
            "rot_x": rot_x,
            "rot_y": rot_y,
            "rot_z": rot_z,
        }
    )
