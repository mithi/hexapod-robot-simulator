import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json

from app import app
from app import HEXAPOD_MEASUREMENTS

# -----------
# Sliders 
# -----------
SLIDER_MARKS = {tick: str(tick) for tick in [-135, -90, -45, 0, 45, 90, 135]}

# HIPS 
HIPS_SLIDERS = [
  dcc.Slider(id='hip-{}'.format(i), min=-135, max=135, marks=SLIDER_MARKS, value=0) for i in range(6)
]

@app.callback(
  Output('pose', 'children'),
  [Input('hip-{}'.format(i), 'value') for i in range(6)]
)
def update_pose(hip0, hip1, hip2, hip3, hip4, hip5):
  return json.dumps({
    '0': hip0,
    '1': hip1,
    '2': hip2,
    '3': hip3,
    '4': hip4,
    '5': hip5,
  })

layout = html.Div([
  html.H3('Kinematics'),
  html.Div(id='sliders-hips', children=HIPS_SLIDERS),
  html.Div(id='display-pose'),
  html.Div(id='pose', style={'display': 'none'})
])

@app.callback(
  Output('display-pose', 'children'),
  [Input('pose', 'children')]
)
def display_pose(angles):
  x = json.loads(angles)  
  return dcc.Markdown('# HELLO! {}'.format(str(x)))
