#-------------------
# Settings
#-------------------
DEBUG_MODE = False
PRINT_POSE_IN_TERMINAL = False

# Too slow?
# set UPDATE_MODE='mouseup'
# This will make widgets only start updating when you release the mouse button
UPDATE_MODE='drag'

# The inverse kinematics solver already updates the points of the hexapod
# but if you want to test whether the pose is indeed correct
# ie use the poses returned by the inverse kinematics solve
# set RECOMPUTE_HEXAPOD to true
# otherwise for faster graph/plot updates, set RECOMPUTE_HEXAPOD to False
RECOMPUTE_HEXAPOD=True

# The range of each leg joint in degrees
ALPHA_MAX_ANGLE = 90
BETA_MAX_ANGLE = 120
GAMMA_MAX_ANGLE = 120
BODY_MAX_ANGLE = 60

LEG_STANCE_MAX_ANGLE = 90
HIP_STANCE_MAX_ANGLE = 45
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


# Pick a number between 0 and 3
# 0 - Using the daq slider UI
# 1 - Using the generic slider UI
# 2 - Using the generic input UI
# 3 - Using the knob UI
# Anything else defaults to Using the daq slider UI
WHICH_POSE_CONTROL_UI = 0

