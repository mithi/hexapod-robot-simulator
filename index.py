from settings import DEBUG_MODE

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import page_inverse, page_kinematics, page_test

server = app.server
# --------------
# Navigation bar partial
# --------------
div_nav = html.Div([
  dcc.Link('Kinematics', href='/kinematics'),
  html.Br(),

  dcc.Link('Inverse Kinematics', href='/inverse-kinematics'),
  html.Br(),

  dcc.Link('Test: Basic Changes', href='/test'),
  html.Br(),

  html.A("Source Code ", href='https://github.com/mithi/hexapod-robot-simulator', target="_blank"),
  html.Br(),
])

# --------------
# Layout
# --------------
app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  html.Div(id='page-content'),
  div_nav,
])

# --------------
# URL redirection
# --------------
PAGES = {
  '/inverse-kinematics': page_inverse.layout,
  '/kinematics': page_kinematics.layout,
  '/test': page_test.layout
}

# --------------
# Display page given URL
# --------------
@app.callback(
  Output('page-content', 'children'),
  [Input('url', 'pathname')]
)
def display_page(pathname):
  try:
    return PAGES[pathname]
  except KeyError:
    return PAGES['/inverse-kinematics']

# --------------
# Run server
# --------------
if __name__ == '__main__':
  app.run_server(
    debug=DEBUG_MODE,
    dev_tools_ui=DEBUG_MODE,
    dev_tools_props_check=DEBUG_MODE
  )