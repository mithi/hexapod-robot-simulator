import os
import dash
from style_settings import DARK_CSS_PATH, LIGHT_CSS_PATH, DARKMODE

external_stylesheets = [DARK_CSS_PATH]
if not DARKMODE:
    external_stylesheets = [LIGHT_CSS_PATH]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Mithi's Hexapod Robot Simulator"
server = app.server
server.secret_key = os.environ.get("secret_key", "secret")
app.config.suppress_callback_exceptions = True
