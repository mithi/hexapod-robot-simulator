from .plotter import HexapodPlot
from .models import VirtualHexapod

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
NAMES_LEG = ['right-middle', 'right-front', 'left-front', 'left-middle', 'left-back', 'right-back']
NAMES_JOINT = ['coxia', 'femur', 'tibia']

BASE_HEXAPOD = VirtualHexapod(100, 100, 100, 100, 100, 100)
BASE_PLOTTER = HexapodPlot()

