import json
from dash.dependencies import Input, Output
from app import app
from settings import WHICH_POSE_CONTROL_UI
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, NAMES_LEG, NAMES_JOINT
from pages import helpers, shared

if WHICH_POSE_CONTROL_UI == 1:
    from widgets.pose_control.generic_daq_slider_ui import SECTION_POSE_CONTROL
elif WHICH_POSE_CONTROL_UI == 2:
    from widgets.pose_control.generic_slider_ui import SECTION_POSE_CONTROL
else:
    from widgets.pose_control.generic_input_ui import SECTION_POSE_CONTROL


# ......................
# Page layout
# ......................

GRAPH_NAME = "graph-kinematics"
ID_MESSAGE_SECTION = "message-kinematics"
ID_PARAMETERS_SECTION = "parameters-kinematics"

sidebar = shared.make_standard_sidebar(
    ID_MESSAGE_SECTION, ID_PARAMETERS_SECTION, SECTION_POSE_CONTROL
)

layout = shared.make_standard_page_layout(GRAPH_NAME, sidebar)


# ......................
# Update page
# ......................

outputs, inputs, states = shared.make_standard_page_inputs_outputs_states(
    GRAPH_NAME, ID_PARAMETERS_SECTION, ID_MESSAGE_SECTION
)


@app.callback(outputs, inputs, states)
def update_kinematics_page(dimensions_json, poses_json, relayout_data, figure):

    dimensions = helpers.load_dimensions(dimensions_json)
    poses = json.loads(poses_json)
    hexapod = VirtualHexapod(dimensions)

    try:
        hexapod.update(poses, assume_ground_targets=False)
    except Exception as alert:
        return figure, helpers.make_alert_message(alert)

    BASE_PLOTTER.update(figure, hexapod)
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


output_parameter = Output(ID_PARAMETERS_SECTION, "children")
input_parameters = input_poses()

# fmt: off

@app.callback(output_parameter, input_parameters)
def update_hexapod_poses(
    rmc, rmf, rmt,
    rfc, rff, rft,
    lfc, lff, lft,
    lmc, lmf, lmt,
    lbc, lbf, lbt,
    rbc, rbf, rbt,
):

    return json.dumps({
        0: {"coxia": rmc or 0, "femur": rmf or 0, "tibia": rmt or 0, "name": "right-middle", "id": 0},
        1: {"coxia": rfc or 0, "femur": rff or 0, "tibia": rft or 0, "name": "right-front", "id": 1},
        2: {"coxia": lfc or 0, "femur": lff or 0, "tibia": lft or 0, "name": "left-front", "id": 2},
        3: {"coxia": lmc or 0, "femur": lmf or 0, "tibia": lmt or 0, "name": "left-middle", "id": 3},
        4: {"coxia": lbc or 0, "femur": lbf or 0, "tibia": lbt or 0, "name": "left-back", "id": 4},
        5: {"coxia": rbc or 0, "femur": rbf or 0, "tibia": rbt or 0, "name": "right-back", "id": 5},
    })

# fmt: on
