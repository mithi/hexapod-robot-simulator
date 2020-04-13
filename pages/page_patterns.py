from settings import UI_CONTROLS_WIDTH, UI_GRAPH_WIDTH, UI_GRAPH_HEIGHT

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from widgets.dimensions_ui import SECTION_DIMENSION_CONTROL
from widgets.leg_patterns_ui import SECTION_LEG_POSE_SLIDERS, LEG_SLIDERS_INPUTS
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER, BASE_FIGURE

import json
from app import app
from pages.shared_callbacks import INPUT_DIMENSIONS_JSON, HIDDEN_BODY_DIMENSIONS
from pages import helpers

# *********************
# *  LAYOUT           *
# *********************
ID_POSES_DIV = "hexapod-poses-values-patterns"
HIDDEN_JOINT_POSES = html.Div(id=ID_POSES_DIV, style={"display": "none"})
SECTION_CONTROLS = [SECTION_DIMENSION_CONTROL, SECTION_LEG_POSE_SLIDERS]

layout = html.Div(
    [
        html.Div(SECTION_CONTROLS, style={"width": UI_CONTROLS_WIDTH}),
        dcc.Graph(
            id="graph-hexapod-3",
            style={"width": UI_GRAPH_WIDTH, "height": UI_GRAPH_HEIGHT},
        ),
        HIDDEN_JOINT_POSES,
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
INPUT_POSES_JSON = Input(ID_POSES_DIV, "children")
OUTPUT = Output("graph-hexapod-3", "figure")
INPUTS = [INPUT_DIMENSIONS_JSON, INPUT_POSES_JSON]
STATES = [State("graph-hexapod-3", "relayoutData"), State("graph-hexapod-3", "figure")]


@app.callback(OUTPUT, INPUTS, STATES)
def update_patterns_page(dimensions_json, poses_json, relayout_data, figure):
    if figure is None:
        return BASE_FIGURE

    dimensions = helpers.load_dimensions(dimensions_json)
    poses = json.loads(poses_json)
    virtual_hexapod = VirtualHexapod(dimensions)
    virtual_hexapod.update(poses)
    BASE_PLOTTER.update(figure, virtual_hexapod)
    helpers.change_camera_view(figure, relayout_data)
    return figure


OUTPUT = Output(ID_POSES_DIV, "children")
INPUTS = LEG_SLIDERS_INPUTS

# ......................
# Update parameters
# ......................
@app.callback(OUTPUT, INPUTS)
def update_poses_alpha_beta_gamma(alpha, beta, gamma):
    return json.dumps(helpers.make_pose(alpha, beta, gamma))
