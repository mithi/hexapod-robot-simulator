from settings import DEBUG_MODE

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import page_inverse, page_kinematics, page_patterns, page_landing

server = app.server
# --------------
# Navigation bar partial
# --------------
div_nav = html.Div(
    [
        html.Br(),
        dcc.Link("🕷️ Kinematics", href="/kinematics"),
        html.Br(),
        dcc.Link("🕷️ Inverse Kinematics", href="/inverse-kinematics"),
        html.Br(),
        dcc.Link("🕷️ Leg Patterns", href="/leg-patterns"),
        html.Br(),
        dcc.Link("🕷️ Root", href="/"),
        html.Br(),
        html.A(
            "👾 Source Code",
            href="https://github.com/mithi/hexapod-robot-simulator",
            target="_blank",
        ),
        html.Br(),
        html.A(
            "☕ Buy Mithi coffee", href="https://ko-fi.com/minimithi", target="_blank"
        ),
    ]
)

# --------------
# Layout
# --------------
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content"), div_nav,]
)

# --------------
# URL redirection
# --------------
PAGES = {
    "/inverse-kinematics": page_inverse.layout,
    "/kinematics": page_kinematics.layout,
    "/leg-patterns": page_patterns.layout,
    "/": page_landing.layout,
}

# --------------
# Display page given URL
# --------------
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    try:
        return PAGES[pathname]
    except KeyError:
        return PAGES["/"]


# --------------
# Run server
# --------------
if __name__ == "__main__":
    app.run_server(
        debug=DEBUG_MODE, dev_tools_ui=DEBUG_MODE, dev_tools_props_check=DEBUG_MODE
    )
