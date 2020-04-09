import json
from dash.dependencies import Output, Input
import dash_html_components as html
from widgets.dimensions_ui import DIMENSION_INPUTS
from app import app

ID_DIMENSIONS_DIV = 'hexapod-dimensions-values'
HIDDEN_BODY_DIMENSIONS = html.Div(id=ID_DIMENSIONS_DIV , style={'display': 'none'})
INPUT_DIMENSIONS_JSON = Input(ID_DIMENSIONS_DIV, 'children')
OUTPUT_DIMENSIONS_JSON = Output(ID_DIMENSIONS_DIV, 'children')
# -------------------
# Listen if the robot dimensions are updated
# -------------------
@app.callback(OUTPUT_DIMENSIONS_JSON, DIMENSION_INPUTS)
def update_hexapod_dimensions_shared(front, side, middle, coxia, femur, tibia):
  dimensions = {
    'front': front or 0,
    'side': side or 0,
    'middle': middle or 0,

    'coxia': coxia or 0,
    'femur': femur or 0,
    'tibia': tibia or 0,
  }
  return json.dumps(dimensions)
