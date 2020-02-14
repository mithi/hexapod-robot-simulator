import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import appinverse, appkinematics

# --------------
# Navigation bar partial
# --------------
div_nav = html.Div([
  dcc.Link('Kinematics', href='/kinematics'),
  html.Br(),
  dcc.Link('Inverse Kinematics', href='/inverse-kinematics'),
  html.Br(),
  dcc.Link('Root', href='/')
])

# --------------
# Layout
# --------------
app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  div_nav,
  html.Div(id='page-content')
])

# --------------
# URL redirection
# --------------
PAGES = {
  '/inverse-kinematics': appinverse.layout,
  '/kinematics': appkinematics.layout,
  '/': "Hello World!"
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
    return '404'

# --------------
# Run server
# --------------
if __name__ == '__main__':
  app.run_server(debug=True)