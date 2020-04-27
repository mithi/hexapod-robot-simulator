import json
from dash.dependencies import Output
from app import app
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER
from widgets.leg_patterns_ui import SECTION_LEG_POSE_SLIDERS, LEG_SLIDERS_INPUTS
from pages import helpers, shared

# ......................
# Page layout
# ......................

GRAPH_NAME = "graph-patterns"
ID_MESSAGE_SECTION = "message-patterns"
ID_PARAMETERS_SECTION = "parameters-patterns"

sidebar = shared.make_standard_sidebar(
    ID_MESSAGE_SECTION, ID_PARAMETERS_SECTION, SECTION_LEG_POSE_SLIDERS
)
layout = shared.make_standard_page_layout(GRAPH_NAME, sidebar)

# ......................
# Update page
# ......................

outputs, inputs, states = shared.make_standard_page_inputs_outputs_states(
    GRAPH_NAME, ID_PARAMETERS_SECTION, ID_MESSAGE_SECTION,
)


@app.callback(outputs, inputs, states)
def update_patterns_page(dimensions_json, poses_json, relayout_data, figure):

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


# ......................
# Update parameters
# ......................

output_parameter = Output(ID_PARAMETERS_SECTION, "children")
input_parameters = LEG_SLIDERS_INPUTS


@app.callback(output_parameter, input_parameters)
def update_poses_alpha_beta_gamma(alpha, beta, gamma):
    return json.dumps(helpers.make_pose(alpha, beta, gamma))
