import json
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash_html_components as html
from app import app
from settings import (
    UI_CONTROLS_WIDTH,
    UI_GRAPH_WIDTH,
    UI_GRAPH_HEIGHT,
)
from widgets.dimensions_ui import DIMENSION_CALLBACK_INPUTS, DIMENSIONS_WIDGETS_SECTION
from hexapod.const import BASE_FIGURE


# ......................
# Update hexapod dimensions callback
# ......................

DIMENSIONS_SECTION_ID = "hexapod-dimensions-values"
DIMENSIONS_HIDDEN_SECTION = html.Div(
    id=DIMENSIONS_SECTION_ID, style={"display": "none"}
)
DIMS_JSON_CALLBACK_INPUT = Input(DIMENSIONS_SECTION_ID, "children")
DIMS_JSON_CALLBACK_OUTPUT = Output(DIMENSIONS_SECTION_ID, "children")


@app.callback(DIMS_JSON_CALLBACK_OUTPUT, DIMENSION_CALLBACK_INPUTS)
def update_hexapod_dimensions_shared(front, side, middle, coxia, femur, tibia):
    dimensions = {
        "front": front or 0,
        "side": side or 0,
        "middle": middle or 0,
        "coxia": coxia or 0,
        "femur": femur or 0,
        "tibia": tibia or 0,
    }
    return json.dumps(dimensions)


# ......................
# Make uniform layout
# Graph on the right, controls on the left
# ......................


def make_standard_page_layout(graph_name, section_controls):
    layout = html.Div(
        [
            html.Div(section_controls, style={"width": UI_CONTROLS_WIDTH}),
            dcc.Graph(
                id=graph_name,
                figure=BASE_FIGURE,
                style={"width": UI_GRAPH_WIDTH, "height": UI_GRAPH_HEIGHT},
            ),
        ],
        style={"display": "flex"},
    )
    return layout


# ......................
# Make standard sidebar
# ......................


def make_standard_page_sidebar(
    message_section_id, parameters_hidden_section_id, parameter_widgets_section
):
    parameters_hidden_section = html.Div(
        id=parameters_hidden_section_id, style={"display": "none"}
    )
    message_section = html.Div(id=message_section_id)

    return [
        DIMENSIONS_WIDGETS_SECTION,
        parameter_widgets_section,
        message_section,
        DIMENSIONS_HIDDEN_SECTION,
        parameters_hidden_section,
    ]


# ......................
# Make input and outputs states for page callback
# .....................


def make_standard_page_callback_params(graph_id, params_section_id, message_section_id):

    message_callback_output = Output(message_section_id, "children")
    params_json_callback_input = Input(params_section_id, "children")
    outputs = [Output(graph_id, "figure"), message_callback_output]
    inputs = [DIMS_JSON_CALLBACK_INPUT, params_json_callback_input]
    states = [State(graph_id, "relayoutData"), State(graph_id, "figure")]
    return outputs, inputs, states
