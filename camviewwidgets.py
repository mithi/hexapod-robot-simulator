import dash_core_components as dcc
from sectioning import make_section_type4, make_section_type3

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
  return dcc.Input(id=_name, type='number', value=_value, step=0.005, style={'marginRight': '5%', 'width': '95%', 'marginBottom': '5%'})

# Camera view adjustment inputs
INPUT_CAMVIEW = {
  'up-x': make_number_input('input-view-up-x', 0.0),
  'up-y': make_number_input('input-view-up-y', 0.0),
  'up-z': make_number_input('input-view-up-z', 1.0),

  'center-x': make_number_input('input-view-center-x', -0.05),
  'center-y': make_number_input('input-view-center-y', 0.0),
  'center-z': make_number_input('input-view-center-z', -0.1),

  'eye-x': make_number_input('input-view-eye-x', 0.35),
  'eye-y': make_number_input('input-view-eye-y', 0.7),
  'eye-z': make_number_input('input-view-eye-z', 0.5),
}

# section for camera view adjustments
section_input_up = make_section_type4(dcc.Markdown('`(UP)`'), INPUT_CAMVIEW['up-x'], INPUT_CAMVIEW['up-y'], INPUT_CAMVIEW['up-z'])
section_input_center = make_section_type4(dcc.Markdown('`(CNTR)`'), INPUT_CAMVIEW['center-x'], INPUT_CAMVIEW['center-y'], INPUT_CAMVIEW['center-z'])
section_input_eye = make_section_type4(dcc.Markdown('`(EYE)`'), INPUT_CAMVIEW['eye-x'], INPUT_CAMVIEW['eye-y'], INPUT_CAMVIEW['eye-z'])
SECTION_INPUT_CAMVIEW = make_section_type3(section_input_up, section_input_center, section_input_eye)