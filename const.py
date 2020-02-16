from hexaplot import HexapodPlot
from hexapod import VirtualHexapod

NAMES_LEG = ['right-middle', 'right-front', 'left-front', 'left-middle', 'left-back', 'right-back']
NAMES_JOINT = ['coxia', 'femur', 'tibia']

BASE_HEXAPOD = VirtualHexapod(100, 100, 100, 100, 100, 100)
BASE_HEXAPLOT = HexapodPlot(BASE_HEXAPOD)

