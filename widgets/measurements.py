import dash_core_components as dcc
import dash_html_components as html
from .sectioning import make_section_type3

INPUT_LENGTHS_IDs = [
  'input-length-front',
  'input-length-side',
  'input-length-middle',

  'input-length-coxia',
  'input-length-femur',
  'input-length-tibia',
]

# -----------
# NUMBER INPUTS FOR HEXAPOD MEASUREMENTS
# -----------
def make_positive_number_input(_name, _value):
  return dcc.Input(id=_name, type='number', value=_value, step=5, min=0, style={'marginRight': '5%', 'width': '95%', 'marginBottom': '5%'})

# Hexapod measured lengths inputs
INPUT_LENGTHS = {
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
section_input_body = make_section_type3(INPUT_LENGTHS['front'], INPUT_LENGTHS['middle'], INPUT_LENGTHS['side'], 'front', 'middle', 'side')
section_input_leg = make_section_type3(INPUT_LENGTHS['coxia'], INPUT_LENGTHS['femur'], INPUT_LENGTHS['tibia'], 'coxia', 'femur', 'tibia')

SECTION_INPUT_LENGTHS = html.Div([
  html.Div(section_input_body, style={'width':  '50%'}),
  html.Div(section_input_leg, style={'width': '50%'}),
  ],
  style={'display': 'flex'}
)

SECTION_LENGTHS_CONTROL = html.Div([
  html.H4('Hexapod Robot Measurements'),
  SECTION_INPUT_LENGTHS,
  html.Br(),
])