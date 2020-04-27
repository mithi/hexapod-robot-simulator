import json
from dash.dependencies import Output
from app import app
from settings import RECOMPUTE_HEXAPOD
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER
from hexapod.ik_solver.ik_solver2 import inverse_kinematics_update
from hexapod.ik_solver.recompute_hexapod import recompute_hexapod
from widgets.ik_ui import SECTION_IK, IK_INPUTS
from pages import helpers, shared

# ......................
# Page layout
# ......................

GRAPH_NAME = "graph-inverse"
ID_MESSAGE_SECTION = "message-inverse"
ID_PARAMETERS_SECTION = "parameters-inverse"

sidebar = shared.make_standard_sidebar(
    ID_MESSAGE_SECTION, ID_PARAMETERS_SECTION, SECTION_IK
)

layout = shared.make_standard_page_layout(GRAPH_NAME, sidebar)

# fmt: off

# ......................
# Update page
# ......................

outputs, inputs, states = shared.make_standard_page_inputs_outputs_states(
    GRAPH_NAME, ID_PARAMETERS_SECTION, ID_MESSAGE_SECTION
)


@app.callback(outputs, inputs, states)
def update_inverse_page(dimensions_json, ik_parameters_json, relayout_data, figure):

    dimensions = helpers.load_dimensions(dimensions_json)
    ik_parameters = json.loads(ik_parameters_json)
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

output_parameter = Output(ID_PARAMETERS_SECTION, "children")
input_parameters = IK_INPUTS


@app.callback(output_parameter, input_parameters)
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
