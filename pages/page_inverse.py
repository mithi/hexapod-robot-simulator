import json
from dash.dependencies import Output
from app import app
from settings import RECOMPUTE_HEXAPOD
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER
from hexapod.ik_solver.ik_solver2 import inverse_kinematics_update
from hexapod.ik_solver.recompute_hexapod import recompute_hexapod
from widgets.ik_ui import IK_WIDGETS_SECTION, IK_CALLBACK_INPUTS
from pages import helpers, shared


# ......................
# Page layout
# ......................

GRAPH_ID = "graph-inverse"
MESSAGE_SECTION_ID = "message-inverse"
PARAMETERS_SECTION_ID = "parameters-inverse"

sidebar = shared.make_standard_page_sidebar(
    MESSAGE_SECTION_ID, PARAMETERS_SECTION_ID, IK_WIDGETS_SECTION
)

layout = shared.make_standard_page_layout(GRAPH_ID, sidebar)


# ......................
# Update page
# ......................

outputs, inputs, states = shared.make_standard_page_callback_params(
    GRAPH_ID, PARAMETERS_SECTION_ID, MESSAGE_SECTION_ID
)


@app.callback(outputs, inputs, states)
def update_inverse_page(dimensions_json, ik_parameters_json, relayout_data, figure):

    dimensions = helpers.load_params(dimensions_json, "dims")
    ik_parameters = helpers.load_params(ik_parameters_json, "ik")
    hexapod = VirtualHexapod(dimensions)

    try:
        poses, hexapod = inverse_kinematics_update(hexapod, ik_parameters)
    except Exception as alert:
        return figure, helpers.make_alert_message(alert)

    if RECOMPUTE_HEXAPOD:
        try:
            hexapod = recompute_hexapod(dimensions, ik_parameters, poses)
        except Exception as alert:
            return figure, helpers.make_alert_message(alert)

    BASE_PLOTTER.update(figure, hexapod)
    helpers.change_camera_view(figure, relayout_data)
    return figure, helpers.make_poses_message(poses)


# ......................
# Update parameters
# ......................

output_parameter = Output(PARAMETERS_SECTION_ID, "children")
input_parameters = IK_CALLBACK_INPUTS


@app.callback(output_parameter, input_parameters)
def update_ik_parameters(
    hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z
):

    return json.dumps(
        {
            "hip_stance": hip_stance or 0,
            "leg_stance": leg_stance or 0,
            "percent_x": percent_x or 0,
            "percent_y": percent_y or 0,
            "percent_z": percent_z or 0,
            "rot_x": rot_x or 0,
            "rot_y": rot_y or 0,
            "rot_z": rot_z or 0,
        }
    )
