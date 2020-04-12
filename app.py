import dash
import os
from style_settings import DARK_CSS_PATH, LIGHT_CSS_PATH, DARKMODE

if DARKMODE:
    external_stylesheets = [DARK_CSS_PATH]
else:
    external_stylesheets = [LIGHT_CSS_PATH]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Mithi's Hexapod Robot Simulator"
server = app.server
server.secret_key = os.environ.get("secret_key", "secret")
app.config.suppress_callback_exceptions = True
