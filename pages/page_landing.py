import dash_core_components as dcc
import dash_html_components as html

from app import app

img1 = html.Img(src='https://mithi.github.io/robotics-blog/robot-only-x1.gif', style={'width': '100%', 'height': 'auto'})
img2 = html.Img(src='https://mithi.github.io/robotics-blog/robot-only-x2.gif', style={'width': '100%', 'height': 'auto'})
img3 = html.Img(src='https://mithi.github.io/robotics-blog/robot-only-x3.gif', style={'width': '100%', 'height': 'auto'})
img4 = html.Img(src='https://mithi.github.io/robotics-blog/robot-only-x4.gif', style={'width': '100%', 'height': 'auto'})

imgA = html.Img(src='https://mithi.github.io/robotics-blog/UI-1.gif', style={'width': '100%', 'height': 'auto'})
imgB = html.Img(src='https://mithi.github.io/robotics-blog/UI-2.gif', style={'width': '100%', 'height': 'auto'})

img_row1 = html.Div([
  html.Div(img1, style={'width': '8%', 'height': 'auto'}),
  html.Div(img2, style={'width': '10%', 'height': 'auto'}),
  html.Div(img3, style={'width': '10%', 'height': 'auto'}),
  html.Div(img4, style={'width': '10%', 'height': 'auto'}),

  ],
  style={'display': 'flex', 'flex-direction': 'row'}
)

img_row2 = html.Div([
  html.Div(imgA, style={'width': '40%', 'height': 'auto'}),
  html.Div(imgB, style={'width': '53%', 'height': 'auto'}),
  html.Div(html.Br(), style={'width': '10%', 'height': 'auto'}),
  ],
  style={'display': 'flex', 'flex-direction': 'row'}
)

layout = html.Div([img_row1, img_row2])
