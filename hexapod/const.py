from .plotter import HexapodPlot
from .models import VirtualHexapod, Hexagon, Linkage
from .templates.figure_template import HEXAPOD_FIGURE
from .templates.pose_template import HEXAPOD_POSE
from .templates.pose_template import PREDEFINED_POSES
from settings import (
  ALPHA_MAX_ANGLE,
  BETA_MAX_ANGLE,
  GAMMA_MAX_ANGLE,
  BODY_MAX_ANGLE,
  HIP_STANCE_MAX_ANGLE,
  LEG_STANCE_MAX_ANGLE
)

# The leg names in leg names start with right middle leg and ends with right back leg (x0 to x5)
#         x2          x1
#          \         /
#           *---*---*
#          /    |    \
#         /     |     \
#        /      |      \
#  x3 --*------cog------*-- x0
#        \      |      /
#         \     |     /
#          \    |    /
#           *---*---*
#          /         \
#         x4         x5
NAMES_LEG = Hexagon.VERTEX_NAMES
NAMES_JOINT = Linkage.POINT_NAMES

BASE_HEXAPOD = VirtualHexapod().new(100, 100, 100, 100, 100, 100)
BASE_PLOTTER = HexapodPlot()
