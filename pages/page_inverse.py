import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import HEXAPOD_MEASUREMENTS

layout = html.Div([
  html.H3('Measurements'),
  dcc.Dropdown(
    id='measurement-dropdown',
    options=[
      {'label': i, 'value': i} for i in ['front_length', 'side_length', 'mid_length']
    ]
  ),
  html.Div(id='measurement-display')
])


@app.callback(
  Output('measurement-display', 'children'),
  [Input('measurement-dropdown', 'value')])
def display_measurement(key):
  try:
    value = HEXAPOD_MEASUREMENTS[key]
    return dcc.Markdown('### {} : {}'.format(key, value))
  except KeyError:
    return "Nothing"