import json
from dash.dependencies import Output
from app import app
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER
from widgets.leg_patterns_ui import PATTERNS_WIDGETS_SECTION, PATTERNS_CALLBACK_INPUTS
from pages import helpers, shared


# ......................
# Page layout
# ......................

GRAPH_ID = "graph-patterns"
MESSAGE_SECTION_ID = "message-patterns"
PARAMETERS_SECTION_ID = "parameters-pattens"

sidebar = shared.make_standard_page_sidebar(
    MESSAGE_SECTION_ID, PARAMETERS_SECTION_ID, PATTERNS_WIDGETS_SECTION
)

layout = shared.make_standard_page_layout(GRAPH_ID, sidebar)


# ......................
# Update page
# ......................

outputs, inputs, states = shared.make_standard_page_callback_params(
    GRAPH_ID, PARAMETERS_SECTION_ID, MESSAGE_SECTION_ID
)


@app.callback(outputs, inputs, states)
def update_patterns_page(dimensions_json, poses_json, relayout_data, figure):

    dimensions = helpers.load_params(dimensions_json, "dims")
    poses = helpers.load_params(poses_json, "pose")
    hexapod = VirtualHexapod(dimensions)

    try:
        hexapod.update(poses)
    except Exception as alert:
        return figure, helpers.make_alert_message(alert)

    BASE_PLOTTER.update(figure, hexapod)
    helpers.change_camera_view(figure, relayout_data)
    return figure, ""


# ......................
# Update parameters
# ......................

output_parameter = Output(PARAMETERS_SECTION_ID, "children")
input_parameters = PATTERNS_CALLBACK_INPUTS


@app.callback(output_parameter, input_parameters)
def update_poses_alpha_beta_gamma(alpha, beta, gamma):
    return json.dumps(helpers.make_pose(alpha, beta, gamma))
