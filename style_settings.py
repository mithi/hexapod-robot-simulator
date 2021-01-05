DARKMODE = True

DARK_CSS_PATH = "https://mithi.github.io/hexapod-robot-simulator/dark.css"
LIGHT_CSS_PATH = "https://mithi.github.io/hexapod-robot-simulator/light.css"

EXTERNAL_STYLESHEETS = [DARK_CSS_PATH]
if not DARKMODE:
    EXTERNAL_STYLESHEETS = [LIGHT_CSS_PATH]


# ***************************************
# GLOBAL PAGE STYLE
# ***************************************

DARK_BG_COLOR = "#222f3e"
DARK_FONT_COLOR = "#32ff7e"

GLOBAL_PAGE_STYLE = {
    "background": DARK_BG_COLOR,
    "color": DARK_FONT_COLOR,
    "padding": "0em",
}

if not DARKMODE:
    GLOBAL_PAGE_STYLE = {"background": "#ffffff", "color": "#2c3e50", "padding": "0em"}


# ***************************************
# NUMBER FIELD INPUT WIDGET
# ***************************************

NUMBER_INPUT_STYLE = {
    "marginRight": "5%",
    "width": "95%",
    "marginBottom": "5%",
    "borderRadius": "10px",
    "border": "solid 1px",
    "fontFamily": "Courier New",
}

if DARKMODE:
    NUMBER_INPUT_STYLE["backgroundColor"] = "#2c3e50"
    NUMBER_INPUT_STYLE["color"] = "#2ecc71"
    NUMBER_INPUT_STYLE["borderColor"] = "#2980b9"


# ***************************************
# DAQ SLIDER INPUT WIDGET
# ***************************************

IK_SLIDER_SIZE = 100

SLIDER_THEME = {
    "dark": DARKMODE,
    "detail": "#ffffff",
    "primary": "#ffffff",
    "secondary": "#ffffff",
}

SLIDER_HANDLE_COLOR = "#2ecc71"
SLIDER_COLOR = "#FC427B"

if not DARKMODE:
    SLIDER_HANDLE_COLOR = "#2c3e50"
    SLIDER_COLOR = "#8e44ad"


# ***************************************
# HEXAPOD GRAPH
# ***************************************

BODY_MESH_COLOR = "#ff6348"
BODY_MESH_OPACITY = 0.3
BODY_COLOR = "#FC427B"
BODY_OUTLINE_WIDTH = 12
COG_COLOR = "#32ff7e"
COG_SIZE = 14
HEAD_SIZE = 14
LEG_COLOR = "#EE5A24"  # "#b71540"
LEG_OUTLINE_WIDTH = 10
SUPPORT_POLYGON_MESH_COLOR = "#3c6382"
SUPPORT_POLYGON_MESH_OPACITY = 0.2
LEGENDS_BG_COLOR = "rgba(44, 62, 80, 0.8)"
AXIS_ZERO_LINE_COLOR = "#079992"
PAPER_BG_COLOR = "#222f3e"
GROUND_COLOR = "#0a3d62"
LEGEND_FONT_COLOR = "#2ecc71"

if not DARKMODE:
    BODY_MESH_COLOR = "#8e44ad"
    BODY_MESH_OPACITY = 0.9
    BODY_COLOR = "#8e44ad"
    BODY_OUTLINE_WIDTH = 10
    COG_COLOR = "#2c3e50"
    COG_SIZE = 15
    HEAD_COLOR = "#8e44ad"
    HEAD_SIZE = 12
    LEG_COLOR = "#2c3e50"
    LEG_OUTLINE_WIDTH = 10
    SUPPORT_POLYGON_MESH_COLOR = "#ffa801"
    SUPPORT_POLYGON_MESH_OPACITY = 0.3
    LEGENDS_BG_COLOR = "rgba(255, 255, 255, 0.5)"
    AXIS_ZERO_LINE_COLOR = "#ffa801"
    PAPER_BG_COLOR = "white"
    GROUND_COLOR = "rgb(240, 240, 240)"
    LEGEND_FONT_COLOR = "#34495e"
