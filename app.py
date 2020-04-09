import dash
import os

external_stylesheets = ["https://codepen.io/mithi-the-encoder/pen/BaoBOKa.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
server.secret_key = os.environ.get("secret_key", "secret")
app.config.suppress_callback_exceptions = True
