import os
import dash
from texts import APP_TITLE
from style_settings import EXTERNAL_STYLESHEETS

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
app.title = APP_TITLE
server = app.server
server.secret_key = os.environ.get("secret_key", "secret")
app.config.suppress_callback_exceptions = True
