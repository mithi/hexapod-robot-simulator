# Used to make html divisions
import dash_html_components as html


def make_section_type3(div1, div2, div3, name1="", name2="", name3=""):
    return html.Div(
        [
            html.Div([div1, name1], style={"width": "33%"}),
            html.Div([div2, name2], style={"width": "33%"}),
            html.Div([div3, name3], style={"width": "33%"}),
        ],
        style={"display": "flex"},
    )


def make_section_type4(div1, div2, div3, div4):
    return html.Div(
        [
            html.Div(div1, style={"width": "16%"}),
            html.Div(div2, style={"width": "28%"}),
            html.Div(div3, style={"width": "28%"}),
            html.Div(div4, style={"width": "28%"}),
        ],
        style={"display": "flex"},
    )


def make_section_type2(div1, div2):
    return html.Div(
        [
            html.Div(div1, style={"width": "50%"}),
            html.Div(div2, style={"width": "50%"}),
        ],
        style={"display": "flex"},
    )


def make_section_type6(div1, div2, div3, div4, div5, div6):
    return html.Div(
        [
            html.Div(div1, style={"width": "17%"}),
            html.Div(div2, style={"width": "17%"}),
            html.Div(div3, style={"width": "17%"}),
            html.Div(div4, style={"width": "17%"}),
            html.Div(div5, style={"width": "16%"}),
            html.Div(div6, style={"width": "16%"}),
        ],
        style={"display": "flex"},
    )
