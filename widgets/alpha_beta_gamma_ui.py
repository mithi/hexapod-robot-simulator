# Widgets used to control the leg pose of all legs uniformly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from settings import ALPHA_MAX_ANGLE, BETA_MAX_ANGLE, GAMMA_MAX_ANGLE
from settings import UPDATE_MODE

SLIDERS_TEST_IDs = ['slider-alpha', 'slider-beta', 'slider-gamma']
SLIDERS_TEST_INPUTS = [Input(i, 'value') for i in SLIDERS_TEST_IDs]

SLIDER_ANGLE_MARKS = {tick: str(tick) for tick in [-45, 0, 45]}
def make_slider(slider_name, angle_range):
  return  dcc.Slider(
    id=slider_name,
    value=0,
    min=-angle_range,
    max=angle_range,
    step=5,
    marks=SLIDER_ANGLE_MARKS,
    updatemode=UPDATE_MODE
  )

SLIDER_ALPHA = make_slider('slider-alpha', ALPHA_MAX_ANGLE)
SLIDER_BETA = make_slider('slider-beta', BETA_MAX_ANGLE)
SLIDER_GAMMA = make_slider('slider-gamma', GAMMA_MAX_ANGLE)

section_sliders = html.Div([
  html.Div([dcc.Markdown('`ALPHA`'), SLIDER_ALPHA], style={'width': '33%'}),
  html.Div([dcc.Markdown('`BETA`'), SLIDER_BETA], style={'width': '33%'}),
  html.Div([dcc.Markdown('`GAMMA`'), SLIDER_GAMMA], style={'width': '33%'}),
  ],
  style={'display': 'flex'}
)

header = html.Label(dcc.Markdown('**LEG POSE CONTROL**'))

SECTION_SLIDERS_TEST = html.Div([header, section_sliders])