# ***************************
# Settings
# ***************************

DARKMODE = True

# The range of each leg joint in degrees
ALPHA_MAX_ANGLE = 90
BETA_MAX_ANGLE = 120
GAMMA_MAX_ANGLE = 120
BODY_MAX_ANGLE = 60
# LEG STANCE
# would define the starting leg position used to compute
# the target ground contact for inverse kinematics poses
# femur/ beta = -leg_stance
# tibia/ gamma = leg_stance

# HIP STANCE
# would defined the starting hip position used to compute
# the target ground contact for inverse kinematics poses
# coxia/alpha angle of
#  right_front = -hip_stance
#   left_front = hip_stance
#    left_back = -hip_stance
#   right_back = hip_stance
#  left_middle = 0
# right_middle = 0
LEG_STANCE_MAX_ANGLE = 90
HIP_STANCE_MAX_ANGLE = 45

# Too slow?
# set UPDATE_MODE='mouseup'
# This will make widgets only start updating when you release the mouse button
UPDATE_MODE = "drag"

DEBUG_MODE = True
# The inverse kinematics solver already updates the points of the hexapod
# but if you want to test whether the pose is indeed correct
# ie use the poses returned by the inverse kinematics solver
# set RECOMPUTE_HEXAPOD to true
# otherwise for faster graph/plot updates, set RECOMPUTE_HEXAPOD to False
# Useful for debugging
RECOMPUTE_HEXAPOD = True

PRINT_IK_LOCAL_LEG = False
PRINT_IK = False
PRINT_MODEL_ON_UPDATE = False
PRINT_MODEL_POSE_ON_UPDATE = False

# 1 - Using the generic slider UI
# 2 - Using the generic input UI
# Anything else defaults to Using the daq slider UI
WHICH_POSE_CONTROL_UI = 2

UI_GRAPH_HEIGHT = "600px"
UI_GRAPH_WIDTH = "63%"
UI_CONTROLS_WIDTH = "37%"

if DARKMODE == True:
    BODY_MESH_COLOR = "#ff6348"
    BODY_MESH_OPACITY = 0.3
    BODY_COLOR = "#FC427B"
    BODY_OUTLINE_WIDTH = 12
    COG_COLOR = "#32ff7e"
    COG_SIZE = 14
    HEAD_SIZE = 14
    LEG_COLOR = "#EE5A24" #"#b71540"
    LEG_OUTLINE_WIDTH = 10
    SUPPORT_POLYGON_MESH_COLOR = "#3c6382"
    SUPPORT_POLYGON_MESH_OPACITY = 0.2
    LEGENDS_BG_COLOR = "rgba(255, 255, 255, 0.5)"
    AXIS_ZERO_LINE_COLOR = "#079992"
    PAPER_BG_COLOR = "#222f3e"
    GROUND_COLOR = "#0a3d62"
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