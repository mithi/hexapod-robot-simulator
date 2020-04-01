import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from widgets.ik_ui import IK_INPUTS, SECTION_IK
from widgets.measurements import SECTION_LENGTHS_CONTROL, MEASURMENT_INPUTS
from app import app

section_nothing = html.Label('Nothing')

SECTION_LEFT = html.Div([
    html.Div([
      html.Label(dcc.Markdown('**INVERSE KINEMATICS CONTROLS**')),
      SECTION_IK,
      SECTION_LENGTHS_CONTROL], style={'width': '60%'}),
    html.Div(section_nothing, style={'width': '40%'}),
  ],
  style={'display': 'flex'}
)


layout = html.Div([
  html.H1('Inverse Kinematics'),
  SECTION_LEFT,
  html.Div(id='ik-variables')
])


inputs = IK_INPUTS + MEASURMENT_INPUTS
@app.callback(
  Output('ik-variables', 'children'),
  inputs)
def display_variables(
  start_hip_stance,
  start_cog_z,
  end_x,
  end_y,
  end_z,
  rot_x,
  rot_y,
  rot_z,
  front,
  side,
  mid,
  coxia,
  femur,
  tibia):

  return dcc.Markdown(f'''
  ```
x: {end_x} | rot.x: {rot_x} | coxia: {coxia} | fro: {front}
y: {end_y} | rot.y: {rot_y} | femur: {femur} | sid: {side}
z: {end_z} | rot.z: {rot_z} | tibia: {tibia} | mid: {mid}
stance: {start_hip_stance} | init.z: {start_cog_z}


  ```
  '''
  )