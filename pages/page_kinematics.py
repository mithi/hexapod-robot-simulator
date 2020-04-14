from settings import (
    UI_CONTROLS_WIDTH,
    UI_GRAPH_WIDTH,
    UI_GRAPH_HEIGHT,
    WHICH_POSE_CONTROL_UI,
)
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, BASE_FIGURE, NAMES_LEG, NAMES_JOINT
from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL
from pages import helpers
from pages.shared_callbacks import INPUT_DIMENSIONS_JSON, SECTION_HIDDEN_BODY_DIMENSIONS
import json
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


if WHICH_POSE_CONTROL_UI == 1:
    from widgets.pose_control.generic_daq_slider_ui import SECTION_POSE_CONTROL
elif WHICH_POSE_CONTROL_UI == 2:
    from widgets.pose_control.generic_slider_ui import SECTION_POSE_CONTROL
else:
    from widgets.pose_control.generic_input_ui import SECTION_POSE_CONTROL

# *********************
# *  LAYOUT           *
# *********************
GRAPH_NAME = "graph-hexapod-kinematics"
ID_MESSAGE_DISPLAY_SECTION = "display-message-kinematics"
SECTION_MESSAGE_DISPLAY = html.Div(id=ID_MESSAGE_DISPLAY_SECTION)
ID_POSES_SECTION = "hexapod-poses-values-kinematics"
SECTION_HIDDEN_JOINT_POSES = html.Div(id=ID_POSES_SECTION, style={"display": "none"})

SECTION_CONTROLS = [
    SECTION_DIMENSION_CONTROL,
    SECTION_POSE_CONTROL,
    SECTION_MESSAGE_DISPLAY,
    SECTION_HIDDEN_JOINT_POSES,
    SECTION_HIDDEN_BODY_DIMENSIONS,
]

layout = html.Div(
    [
        html.Div(SECTION_CONTROLS, style={"width": UI_CONTROLS_WIDTH}),
        dcc.Graph(
            id=GRAPH_NAME, style={"width": UI_GRAPH_WIDTH, "height": UI_GRAPH_HEIGHT},
        ),
    ],
    style={"display": "flex"},
)

# fmt: off
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
def update_kinematics_page(dimensions_json, poses_json, relayout_data, figure):
    if figure is None:
        return BASE_FIGURE, ""

    dimensions = helpers.load_dimensions(dimensions_json)
    poses = json.loads(poses_json)
    virtual_hexapod = VirtualHexapod(dimensions)

    try:
        virtual_hexapod.update(poses)
    except Exception as alert:
        return figure, helpers.make_alert_message(str(alert))

    BASE_PLOTTER.update(figure, virtual_hexapod)
    helpers.change_camera_view(figure, relayout_data)
    return figure, ""


# ......................
# Update Parameters
# ......................
def leg_inputs(leg_name):
    return [
        Input(f"input-{leg_name}-{joint_name}", "value") for joint_name in NAMES_JOINT
    ]


def input_poses():
    inputs_poses = []
    for leg_name in NAMES_LEG:
        inputs_poses += leg_inputs(leg_name)
    return inputs_poses


OUTPUT_POSES = Output(ID_POSES_SECTION, "children")
INPUTS_POSES = input_poses()


@app.callback(OUTPUT_POSES, INPUTS_POSES)
def update_hexapod_poses(
    rmc, rmf, rmt,
    rfc, rff, rft,
    lfc, lff, lft,
    lmc, lmf, lmt,
    lbc, lbf, lbt,
    rbc, rbf, rbt,
):

    return json.dumps(
        {0: {"coxia": rmc or 0, "femur": rmf or 0, "tibia": rmt or 0, "name": "right-middle", "id": 0, },
         1: {"coxia": rfc or 0, "femur": rff or 0, "tibia": rft or 0, "name": "right-front", "id": 1, },
         2: {"coxia": lfc or 0, "femur": lff or 0, "tibia": lft or 0, "name": "left-front", "id": 2, },
         3: {"coxia": lmc or 0, "femur": lmf or 0, "tibia": lmt or 0, "name": "left-middle", "id": 3, },
         4: {"coxia": lbc or 0, "femur": lbf or 0, "tibia": lbt or 0, "name": "left-back", "id": 4, },
         5: {"coxia": rbc or 0, "femur": rbf or 0, "tibia": rbt or 0, "name": "right-back", "id": 5, }, },
    )
# fmt: on
