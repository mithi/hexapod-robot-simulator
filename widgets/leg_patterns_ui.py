# Widgets used to control the leg pose of all legs uniformly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
import dash_daq
from settings import ALPHA_MAX_ANGLE, BETA_MAX_ANGLE, GAMMA_MAX_ANGLE
from settings import UPDATE_MODE

SLIDERS_TEST_IDs = ['slider-alpha', 'slider-beta', 'slider-gamma']
SLIDERS_TEST_INPUTS = [Input(i, 'value') for i in SLIDERS_TEST_IDs]

def make_slider(name, max_angle):
  _, angle = name.split('-')

  return html.Div(dash_daq.Slider( # pylint: disable=not-callable
    id=name,
    min=-max_angle,
    max=max_angle,
    value=10,
    size=300,
    updatemode=UPDATE_MODE,
    handleLabel={"showCurrentValue": True,"label": angle},
    step=2.5),
    style={'padding': '2em 0 2em 0'}
  )

SLIDER_ALPHA = make_slider('slider-alpha', ALPHA_MAX_ANGLE)
SLIDER_BETA = make_slider('slider-beta', BETA_MAX_ANGLE)
SLIDER_GAMMA = make_slider('slider-gamma', GAMMA_MAX_ANGLE)

header = html.Label(dcc.Markdown('**LEG POSE CONTROL**'))

SECTION_SLIDERS_TEST = html.Div([
  header,
  SLIDER_ALPHA,
  SLIDER_BETA,
  SLIDER_GAMMA])