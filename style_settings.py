DARKMODE = True

DARK_CSS_PATH = "https://codepen.io/mithi-the-encoder/pen/BaoBOKa.css"
LIGHT_CSS_PATH = "https://codepen.io/mithi-the-encoder/pen/eYpObwK.css"

# ***************************************
# GLOBAL PAGE STYLE
# ***************************************

GLOBAL_PAGE_STYLE = {}

DARK_BG_COLOR = "#222f3e"
DARK_FONT_COLOR = "#2ecc71"
if DARKMODE:
    GLOBAL_PAGE_STYLE = {"background": DARK_BG_COLOR, "color": DARK_FONT_COLOR}
else:
    GLOBAL_PAGE_STYLE = {"background": '#ffffff'}
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

SLIDER_THEME = {
    "dark": DARKMODE,
    "detail": "#ffffff",
    "primary": "#ffffff",
    "secondary": "#ffffff",
}

SLIDER_HANDLE_COLOR = "#00d8d6"
SLIDER_COLOR = "#05c46b"

# ***************************************
# HEXAPOD GRAPH
# ***************************************
if DARKMODE is True:
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
    LEGEND_FONT_COLOR = "ffffff"
else:
    BODY_MESH_COLOR = "#8e44ad"
    BODY_MESH_OPACITY = 0.6
    BODY_COLOR = "#8e44ad"
    BODY_OUTLINE_WIDTH = 10
    COG_COLOR = "#ff4757"
    COG_SIZE = 12
    HEAD_COLOR = "#8e44ad"
    HEAD_SIZE = 12
    LEG_COLOR = "#2c3e50"
    LEG_OUTLINE_WIDTH = 10
    SUPPORT_POLYGON_MESH_COLOR = "#2ecc71"
    SUPPORT_POLYGON_MESH_OPACITY = 0.2
    LEGENDS_BG_COLOR = "rgba(255, 255, 255, 0.5)"
    AXIS_ZERO_LINE_COLOR = "white"
    PAPER_BG_COLOR = "white"
    GROUND_COLOR = "rgb(240, 240, 240)"
    LEGEND_FONT_COLOR = "#34495e"
