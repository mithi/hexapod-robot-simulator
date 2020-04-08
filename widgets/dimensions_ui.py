# Widgets used to control the dimensions of the hexapod
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from .sectioning import make_section_type3

INPUT_DIMENSIONS_IDs = [
  'input-length-front',
  'input-length-side',
  'input-length-middle',

  'input-length-coxia',
  'input-length-femur',
  'input-length-tibia',
]

DIMENSION_INPUTS = [Input(input_id, 'value') for input_id in INPUT_DIMENSIONS_IDs]

# -----------
# NUMBER INPUTS FOR DIMENSIONS
# -----------
def make_positive_number_input(_name, _value):
  input_style = {'marginRight': '5%', 'width': '95%', 'marginBottom': '5%'}
  return dcc.Input(id=_name, type='number', value=_value, step=5, min=0, style=input_style)

# Hexapod dimension s inputs
INPUT_DIMENSIONS = {
  'front': make_positive_number_input('input-length-front', 100),
  'side': make_positive_number_input('input-length-side', 100),
  'middle': make_positive_number_input('input-length-middle', 100),
  'coxia': make_positive_number_input('input-length-coxia', 100),
  'femur': make_positive_number_input('input-length-femur', 100),
  'tibia': make_positive_number_input('input-length-tibia', 100),
}

# -----------
# PARTIAL SECTIONS
# -----------
# section for hexapod measurement adjustments
section_input_body = make_section_type3(INPUT_DIMENSIONS['front'], INPUT_DIMENSIONS['middle'], INPUT_DIMENSIONS['side'], 'front', 'middle', 'side')
section_input_leg = make_section_type3(INPUT_DIMENSIONS['coxia'], INPUT_DIMENSIONS['femur'], INPUT_DIMENSIONS['tibia'], 'coxia', 'femur', 'tibia')

input_style = {'width':  '50%', 'fontFamily': 'Courier', 'fontSize': '0.9em'}

SECTION_DIMENSION_CONTROL = html.Div([
  html.Label(dcc.Markdown('**HEXAPOD ROBOT DIMENSIONS**')),
  html.Div([
    html.Div(section_input_body, style=input_style),
    html.Div(section_input_leg, style=input_style),
  ], style={'display': 'flex'}),
  html.Br()
])