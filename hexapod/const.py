from copy import deepcopy
from hexapod.plotter import HexapodPlotter
from hexapod.models import VirtualHexapod, Hexagon, Linkage
from hexapod.templates.figure_template import HEXAPOD_FIGURE
from hexapod.templates.pose_template import HEXAPOD_POSE

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


BASE_IK_PARAMS = {
    "hip_stance": 0,
    "leg_stance": 0,
    "percent_x": 0,
    "percent_y": 0,
    "percent_z": 0,
    "rot_x": 0,
    "rot_y": 0,
    "rot_z": 0,
}

BASE_POSE = deepcopy(HEXAPOD_POSE)

BASE_HEXAPOD = VirtualHexapod(BASE_DIMENSIONS)
BASE_PLOTTER = HexapodPlotter()

HEXAPOD = deepcopy(BASE_HEXAPOD)
HEXAPOD.update(HEXAPOD_POSE)
BASE_FIGURE = deepcopy(HEXAPOD_FIGURE)
BASE_PLOTTER.update(BASE_FIGURE, HEXAPOD)
