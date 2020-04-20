from copy import deepcopy
from hexapod.plotter import HexapodPlotter
from hexapod.models import VirtualHexapod, Hexagon, Linkage
from hexapod.templates.figure_template import HEXAPOD_FIGURE
from hexapod.templates.pose_template import HEXAPOD_POSE

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

BASE_DIMENSIONS = {
    "front": 100,
    "side": 100,
    "middle": 100,
    "coxia": 100,
    "femur": 100,
    "tibia": 100,
}

BASE_HEXAPOD = VirtualHexapod(BASE_DIMENSIONS)
BASE_PLOTTER = HexapodPlotter()

HEXAPOD = deepcopy(BASE_HEXAPOD)
HEXAPOD.update(HEXAPOD_POSE)
BASE_FIGURE = deepcopy(HEXAPOD_FIGURE)
BASE_PLOTTER.update(BASE_FIGURE, HEXAPOD)
