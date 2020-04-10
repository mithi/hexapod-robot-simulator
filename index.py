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

header = dcc.Markdown(
    f"""
[👾][1] [☕][2] [🕷️][3] [🕷️](/kinematics) [🕷️](/leg-patterns) [🕷️](/)
[1]: https://github.com/mithi/hexapod-robot-simulator
[2]: https://ko-fi.com/minimithi
[3]: /inverse-kinematics
[4]: /kinematics
[5]: /leg-patterns
[6]: /
"""
)

div_nav = html.Div(
    [
        html.Br(),
        html.A(
            "👾 Source Code",
            href="https://github.com/mithi/hexapod-robot-simulator",
            target="_blank",
        ),
        html.Br(),
        html.A(
            "☕ Buy Mithi coffee", href="https://ko-fi.com/minimithi", target="_blank",
        ),
        html.Br(),
        dcc.Link("🕷️ Root", href="/"),
        html.Br(),
        dcc.Link("🕷️ Inverse Kinematics", href="/inverse-kinematics"),
        html.Br(),
        dcc.Link("🕷️ Kinematics", href="/kinematics"),
        html.Br(),
        dcc.Link("🕷️ Leg Patterns", href="/leg-patterns"),
    ]
)

# --------------
# Layout
# --------------
app.layout = html.Div(
    [
        header,
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        div_nav,
    ],
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