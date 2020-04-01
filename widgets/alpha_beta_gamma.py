import dash_core_components as dcc
import dash_html_components as html

SLIDERS_TEST_IDs = ['slider-alpha', 'slider-beta', 'slider-gamma']
SLIDER_ANGLE_MARKS = {tick: str(tick) for tick in [-90, -45, 0, 45, 90]}
SLIDER_ALPHA = dcc.Slider(id='slider-alpha', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_BETA = dcc.Slider(id='slider-beta', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_GAMMA = dcc.Slider(id='slider-gamma', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)

SECTION_SLIDERS_TEST = html.Div([
  html.Div([html.Label('ALPHA'), SLIDER_ALPHA], style={'width': '33%'}),
  html.Div([html.Label('BETA'), SLIDER_BETA], style={'width': '33%'}),
  html.Div([html.Label('GAMMA'), SLIDER_GAMMA], style={'width': '33%'}),
  ],
  style={'display': 'flex'}
)
