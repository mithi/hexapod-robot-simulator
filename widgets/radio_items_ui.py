import dash_core_components as dcc
import dash_html_components as html
from hexapod.const import PREDEFINED_POSES

section_predefined_pose_control = html.Div([
  html.Label(dcc.Markdown('**PREDEFINED POSES**')),
  dcc.Markdown('❗**`IMPORTANT! `**` Select NONE to listen to custom controls. \
    When a predefined pose is selected, \
    custom leg angles input (alpha/beta/gamma) would be ignored.`'),
  dcc.RadioItems(
  id='predefined-poses',
  options=[{'label': i, 'value': i} for i in PREDEFINED_POSES.keys()],
  value='NONE',
  labelStyle={'display': 'inline-block'}
  ),
  html.Br()
])