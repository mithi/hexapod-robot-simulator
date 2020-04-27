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
from widgets.dimensions_ui import DIMENSION_INPUTS, SECTION_DIMENSION_CONTROL
from hexapod.const import BASE_FIGURE

# ......................
# Update hexapod dimensions callback
# ......................

ID_DIMENSIONS_SECTION = "hexapod-dimensions-values"
SECTION_HIDDEN_BODY_DIMENSIONS = html.Div(
    id=ID_DIMENSIONS_SECTION, style={"display": "none"}
)
INPUT_DIMENSIONS_JSON = Input(ID_DIMENSIONS_SECTION, "children")
OUTPUT_DIMENSIONS_JSON = Output(ID_DIMENSIONS_SECTION, "children")


@app.callback(OUTPUT_DIMENSIONS_JSON, DIMENSION_INPUTS)
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


def make_standard_sidebar(
    message_section_id, hidden_parameters_section_id, section_parameter_widgets
):
    section_hidden_parameters = html.Div(
        id=hidden_parameters_section_id, style={"display": "none"}
    )
    section_message_display = html.Div(id=message_section_id)

    return [
        SECTION_DIMENSION_CONTROL,
        section_parameter_widgets,
        section_message_display,
        SECTION_HIDDEN_BODY_DIMENSIONS,
        section_hidden_parameters,
    ]


# ......................
# Make input and outputs states for page callback
# .....................


def make_standard_page_inputs_outputs_states(
    graph_name, parameters_section_id, message_section_id
):

    output_message_display = Output(message_section_id, "children")
    input_parameters_json = Input(parameters_section_id, "children")
    outputs = [Output(graph_name, "figure"), output_message_display]
    inputs = [INPUT_DIMENSIONS_JSON, input_parameters_json]
    states = [State(graph_name, "relayoutData"), State(graph_name, "figure")]
    return outputs, inputs, states
