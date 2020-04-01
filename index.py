import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import page_inverse, page_kinematics, page_test
# --------------
# Navigation bar partial
# --------------
div_nav = html.Div([
  dcc.Link('Kinematics', href='/kinematics'),
  html.Br(),

  dcc.Link('Inverse Kinematics', href='/inverse-kinematics'),
  html.Br(),

  dcc.Link('Test: basic changes', href='/test'),
  html.Br(),

  dcc.Link('Root', href='/'),
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
    return 'Hello world!'

# --------------
# Run server
# --------------
if __name__ == '__main__':
  app.run_server(
    debug=True,
    dev_tools_ui=False,
    dev_tools_props_check=False
  )