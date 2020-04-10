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
from hexapod.ik_solver import inverse_kinematics_update
from widgets.ik_ui import SECTION_IK, IK_INPUTS
from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL, DIMENSION_INPUTS

import numpy as np
from copy import deepcopy
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
    style={"display": "flex",},
)

# *********************
# *  CALLBACKS        *
# *********************
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
    hexapod = VirtualHexapod(dimensions)
    ik_parameters = json.loads(ik_parameters_json)
    hexapod, poses, alert = inverse_kinematics_update(hexapod, ik_parameters)

    if RECOMPUTE_HEXAPOD and poses:
        hexapod = VirtualHexapod(dimensions)
        hexapod.update(poses)
        hexapod.move_xyz(
            ik_parameters["percent_x"],
            ik_parameters["percent_y"],
            ik_parameters["percent_z"],
        )

    BASE_PLOTTER.update(figure, hexapod)
    helpers.change_camera_view(figure, relayout_data)

    info = helpers.format_info(dimensions, ik_parameters)
    text = helpers.update_display_message(info, poses, alert)

    return figure, helpers.make_monospace(text)
