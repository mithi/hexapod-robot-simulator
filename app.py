import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

HEXAPOD_MEASUREMENTS = {
  'front_length': 20,
  'side_length': 30,
  'mid_length': 40, 
  'hip_length': 25, 
  'knee_length': 40,
  'ankle_length':60
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True