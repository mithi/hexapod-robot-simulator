import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
import dash_daq

IK_INPUT_IDs = [
  'input-start-hip-stance',
  'input-start-leg-stance',
  'input-end-x',
  'input-end-y',
  'input-end-z',
  'input-end-rot-x',
  'input-end-rot-y',
  'input-end-rot-z',
]

def make_translate_slider(name, slider_label, slider_size=120):
  return dash_daq.Slider( # pylint: disable=not-callable
    id=name,
    min=-1.0,
    max=1.0,
    value=0.05,
    size=slider_size,
    updatemode='drag',
    vertical=True,
    handleLabel={"showCurrentValue": True,"label": slider_label},
    step=0.05,
  )

def make_h_slider(name, slider_label):
  return dash_daq.Slider( # pylint: disable=not-callable
    id=name,
    min=-90,
    max=90,
    value=10,
    size=50,
    updatemode='drag',
    vertical=True,
    handleLabel={"showCurrentValue": True,"label": slider_label},
    step=0.05,
  )

def make_rotate_knob(name, knob_label):
  return dash_daq.Knob( # pylint: disable=not-callable
    id=name,
    min=-65,
    max=65,
    value=0,
    size=65,
    scale = {'custom': {0: knob_label, -60: '-60', -30: '-30',  30: '30', 60: '60'}}
  )

def make_stance_slider(name, slider_label):
  return dash_daq.Slider( # pylint: disable=not-callable
    id=name,
    min=0.0,
    max=45.0,
    value=0.0,
    size=50,
    updatemode='drag',
    vertical=True,
    handleLabel={"showCurrentValue": True,"label": slider_label},
    step=5.0,
  )

div_ss = make_stance_slider('input-start-hip-stance', 'hip.stance')
div_sz = make_h_slider('input-start-leg-stance', 'leg.stance')
div_ex = make_translate_slider('input-end-x', 'end.x')
div_ey = make_translate_slider('input-end-y', 'end.y')
div_ez = make_translate_slider('input-end-z', 'end.z')
div_rx = make_rotate_knob('input-end-rot-x', 'rot.x')
div_ry = make_rotate_knob('input-end-rot-y', 'rot.y')
div_rz = make_rotate_knob('input-end-rot-z', 'rot.z')

start_section_ik = html.Div([div_ss, html.Br(), div_sz],)
SECTION_IK = html.Div([
    html.Div(start_section_ik, style={'padding': '0 0 0 4em'}),
    html.Div(div_rx),
    html.Div(div_ex, style={'padding': '0 0 0 2em'}),
    html.Div(div_ry),
    html.Div(div_ey, style={'padding': '0 0 0 2em'}),
    html.Div(div_rz),
    html.Div(div_ez, style={'padding': '0 0 0 2em'}),
  ],
  style={'display': 'flex', 'flex-direction': 'row'}
)

IK_INPUTS = [Input(input_id, 'value') for input_id in IK_INPUT_IDs]
