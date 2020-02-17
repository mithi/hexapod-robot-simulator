from .plotter import HexapodPlot
from .models import VirtualHexapod, Hexagon, Linkage

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

BASE_HEXAPOD = VirtualHexapod(100, 100, 100, 100, 100, 100)
BASE_PLOTTER = HexapodPlot()

