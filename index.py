import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from texts import (
    URL_KOFI,
    URL_REPO,
    KINEMATICS_PAGE_PATH,
    IK_PAGE_PATH,
    PATTERNS_PAGE_PATH,
    ROOT_PATH,
)
from settings import DEBUG_MODE
from style_settings import GLOBAL_PAGE_STYLE
from app import app
from pages import page_inverse, page_kinematics, page_patterns, page_landing

server = app.server

# ....................
# Navigation partials
# ....................
icon_link_style = {"margin": "0 0 0 0.5em"}

div_header = html.Div(
    [
        html.A(html.H6("👾"), href=URL_REPO, target="_blank", style=icon_link_style),
        html.A(html.H6("☕"), href=URL_KOFI, target="_blank", style=icon_link_style),
        dcc.Link(html.H6("●"), href=PATTERNS_PAGE_PATH, style=icon_link_style),
        dcc.Link(html.H6("●"), href=IK_PAGE_PATH, style=icon_link_style),
        dcc.Link(html.H6("●"), href=KINEMATICS_PAGE_PATH, style=icon_link_style),
        dcc.Link(html.H6("●"), href=ROOT_PATH, style=icon_link_style),
    ],
    style={"display": "flex", "flex-direction": "row"},
)

div_footer = html.Div(
    [
        html.A("👾 Source Code", href=URL_REPO, target="_blank"),
        html.Br(),
        html.A("☕ Buy Mithi coffee", href=URL_KOFI, target="_blank"),
        html.Br(),
        dcc.Link("● Leg Patterns", href=PATTERNS_PAGE_PATH),
        html.Br(),
        dcc.Link("● Inverse Kinematics", href=IK_PAGE_PATH),
        html.Br(),
        dcc.Link("● Kinematics", href=KINEMATICS_PAGE_PATH),
        html.Br(),
        dcc.Link("● Root", href=ROOT_PATH),
        html.Br(),
    ],
)

# ....................
# Page layout
# ....................
app.layout = html.Div(
    [
        div_header,
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        div_footer,
    ],
    style=GLOBAL_PAGE_STYLE,
)


# ....................
# URL redirection
# ....................
PAGES = {
    IK_PAGE_PATH: page_inverse.layout,
    KINEMATICS_PAGE_PATH: page_kinematics.layout,
    PATTERNS_PAGE_PATH: page_patterns.layout,
    ROOT_PATH: page_landing.layout,
}


# ....................
# Callback to display page given URL
# ....................
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    try:
        return PAGES[pathname]
    except KeyError:
        return PAGES[ROOT_PATH]


# ....................
# Run server
# ....................
if __name__ == "__main__":
    app.run_server(
        debug=DEBUG_MODE, dev_tools_ui=DEBUG_MODE, dev_tools_props_check=DEBUG_MODE
    )
