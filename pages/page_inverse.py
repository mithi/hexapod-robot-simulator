import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from widgets.ik_ui import IK_INPUT_IDs, SECTION_IK
from app import app

section_nothing = html.Label('Nothing')

SECTION_LEFT = html.Div([
    html.Div(SECTION_IK, style={'width': '60%'}),
    html.Div(section_nothing, style={'width': '40%'}),
  ],
  style={'display': 'flex'}
)


layout = html.Div([
  html.H1('Inverse Kinematics'),
  SECTION_LEFT,
  html.Div(id='ik-variables')
])


ik_inputs = [Input(input_id, 'value') for input_id in IK_INPUT_IDs]
@app.callback(
  Output('ik-variables', 'children'),
  ik_inputs)
def display_variables(
  start_hip_stance,
  start_cog_z,
  end_x,
  end_y,
  end_z,
  rot_x,
  rot_y,
  rot_z):

  return dcc.Markdown(f'''
  ```
x: {end_x} | rot x: {rot_x}
y: {end_y} | rot y: {rot_y}
z: {end_z} | rot z: {rot_z}
stance: {start_hip_stance} | init z: {start_cog_z}
  ```
  '''
  )