import dash_core_components as dcc
from dash.dependencies import Input, Output
from .sectioning import make_section_type4, make_section_type3
from hexapod.const import HEXAPOD_FIGURE

camera = HEXAPOD_FIGURE['layout']['scene']['camera']

CAMVIEW_INPUT_IDs = [
  'input-view-up-x',
  'input-view-up-y',
  'input-view-up-z',

  'input-view-center-x',
  'input-view-center-y',
  'input-view-center-z',

  'input-view-eye-x',
  'input-view-eye-y',
  'input-view-eye-z',
]

# -----------
# CAMERA VIEW
# -----------
def make_number_input(_name, _value):
  return dcc.Input(id=_name, type='number', value=_value, style={'marginRight': '5%', 'width': '95%', 'marginBottom': '5%'})

# Camera view adjustment inputs
INPUT_CAMVIEW = {
  'up-x': make_number_input('input-view-up-x', camera['up']['x']),
  'up-y': make_number_input('input-view-up-y', camera['up']['y']),
  'up-z': make_number_input('input-view-up-z', camera['up']['z']),

  'center-x': make_number_input('input-view-center-x', camera['center']['x']),
  'center-y': make_number_input('input-view-center-y', camera['center']['y']),
  'center-z': make_number_input('input-view-center-z', camera['center']['z']),

  'eye-x': make_number_input('input-view-eye-x', camera['eye']['x']),
  'eye-y': make_number_input('input-view-eye-y', camera['eye']['y']),
  'eye-z': make_number_input('input-view-eye-z', camera['eye']['z']),
}

# section for camera view adjustments
section_input_up = make_section_type4(dcc.Markdown('`(UP)`'), INPUT_CAMVIEW['up-x'], INPUT_CAMVIEW['up-y'], INPUT_CAMVIEW['up-z'])
section_input_center = make_section_type4(dcc.Markdown('`(CNTR)`'), INPUT_CAMVIEW['center-x'], INPUT_CAMVIEW['center-y'], INPUT_CAMVIEW['center-z'])
section_input_eye = make_section_type4(dcc.Markdown('`(EYE)`'), INPUT_CAMVIEW['eye-x'], INPUT_CAMVIEW['eye-y'], INPUT_CAMVIEW['eye-z'])
SECTION_INPUT_CAMVIEW = make_section_type3(section_input_up, section_input_center, section_input_eye)
CAMVIEW_OUTPUTS = [Output(i, 'value') for i in CAMVIEW_INPUT_IDs]
CAMVIEW_INPUTS = [Input(i, 'value') for i in CAMVIEW_INPUT_IDs]
