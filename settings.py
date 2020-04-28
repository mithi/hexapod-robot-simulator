# ***************************
# Settings
# ***************************

# The range of each leg joint in degrees
ALPHA_MAX_ANGLE = 90
BETA_MAX_ANGLE = 180
GAMMA_MAX_ANGLE = 180
BODY_MAX_ANGLE = 40

# LEG STANCE
# would define the starting leg position used to compute
# the target ground contact for inverse kinematics poses
# femur/ beta = -leg_stance
# tibia/ gamma = leg_stance
LEG_STANCE_MAX_ANGLE = 90

# HIP STANCE
# would defined the starting hip position used to compute
# the target ground contact for inverse kinematics poses
# coxia/alpha angle of
#  right_front = -hip_stance
#   left_front = +hip_stance
#    left_back = -hip_stance
#   right_back = +hip_stance
#  left_middle = 0
# right_middle = 0
HIP_STANCE_MAX_ANGLE = 45

# Too slow? set UPDATE_MODE='mouseup'
# Makes widgets only start updating when you release the mouse button
UPDATE_MODE = "drag"

DEBUG_MODE = False
ASSERTION_ENABLED = False

# The inverse kinematics solver already updates the points of the hexapod
# But there is no guarantee that this pose is correct
# So better update a fresh hexapod with the resulting poses
RECOMPUTE_HEXAPOD = True

PRINT_IK_LOCAL_LEG = False
PRINT_IK = False
PRINT_MODEL_ON_UPDATE = False

# 1 - Use the daq slider UI
# 2 - Use the generic slider UI
# Anything else defaults to the generic input UI, which I prefer
WHICH_POSE_CONTROL_UI = 0

# Make it more granular to prevent overloading the server
SLIDER_ANGLE_RESOLUTION = 1.5
INPUT_DIMENSIONS_RESOLUTION = 1

UI_GRAPH_HEIGHT = "600px"
UI_GRAPH_WIDTH = "63%"
UI_SIDEBAR_WIDTH = "37%"
