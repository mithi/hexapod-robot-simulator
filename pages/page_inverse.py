from settings import (
    RECOMPUTE_HEXAPOD,
    UI_CONTROLS_WIDTH,
    UI_GRAPH_WIDTH,
    UI_GRAPH_HEIGHT,
)

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, BASE_FIGURE
from hexapod.ik_solver.ik_solver import inverse_kinematics_update
from hexapod.ik_solver.recompute_hexapod import recompute_hexapod
from widgets.ik_ui import SECTION_IK, IK_INPUTS
from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL

import json
from app import app
from pages.shared_callbacks import INPUT_DIMENSIONS_JSON, HIDDEN_BODY_DIMENSIONS
from pages import helpers

# *********************
# *  LAYOUT           *
# *********************
ID_MESSAGE_DISPLAY_DIV = "display-message-div"
ID_IK_PARAMETERS_DIV = "ik-parameters"
HIDDEN_IK_PARAMETERS = html.Div(id=ID_IK_PARAMETERS_DIV, style={"display": "none"})

SECTION_CONTROLS = [
    SECTION_DIMENSION_CONTROL,
    SECTION_IK,
    html.Div(id=ID_MESSAGE_DISPLAY_DIV),
    HIDDEN_IK_PARAMETERS,
]

layout = html.Div(
    [
        html.Div(SECTION_CONTROLS, style={"width": UI_CONTROLS_WIDTH}),
        dcc.Graph(
            id="graph-hexapod-2",
            style={"width": UI_GRAPH_WIDTH, "height": UI_GRAPH_HEIGHT},
        ),
        HIDDEN_BODY_DIMENSIONS,
    ],
    style={"display": "flex"},
)


# *********************
# *  CALLBACKS        *
# *********************

# ......................
# Update page
# ......................
OUTPUTS = [
    Output("graph-hexapod-2", "figure"),
    Output(ID_MESSAGE_DISPLAY_DIV, "children"),
]
INPUTS = [INPUT_DIMENSIONS_JSON, Input(ID_IK_PARAMETERS_DIV, "children")]
STATES = [State("graph-hexapod-2", "relayoutData"), State("graph-hexapod-2", "figure")]


@app.callback(OUTPUTS, INPUTS, STATES)
def update_inverse_page(dimensions_json, ik_parameters_json, relayout_data, figure):
    if figure is None:
        return BASE_FIGURE, ""

    dimensions = helpers.load_dimensions(dimensions_json)
    ik_parameters = json.loads(ik_parameters_json)
    hexapod = VirtualHexapod(dimensions)

    try:
        hexapod, poses = inverse_kinematics_update(hexapod, ik_parameters)
    except Exception as alert:
        return figure, helpers.make_alert_message(str(alert))

    if RECOMPUTE_HEXAPOD:
        hexapod = recompute_hexapod(dimensions, ik_parameters, poses)

    BASE_PLOTTER.update(figure, hexapod)
    helpers.change_camera_view(figure, relayout_data)
    return figure, helpers.make_poses_message(poses)


# ......................
# Update parameters
# ......................
OUTPUT = Output(ID_IK_PARAMETERS_DIV, "children")


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
