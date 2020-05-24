import dash_html_components as html
from texts import URL_IMG_LANDING

img = html.Img(src=URL_IMG_LANDING, style={"width": "100%", "height": "auto"},)

layout = html.Div(
    [
        html.Div(img, style={"width": "20%", "height": "auto"}),
        html.Div(html.Br(), style={"width": "auto", "height": "auto"}),
    ],
    style={"display": "flex", "flex-direction": "row"},
)
