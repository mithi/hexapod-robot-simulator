import dash_core_components as dcc
from hexapod.const import BASE_PLOTTER
from hexapod.const import HEXAPOD_POSE, NAMES_LEG, BASE_DIMENSIONS
from copy import deepcopy
import json


def change_camera_view(figure, relayout_data):
    # Use current camera view to display plot
    if relayout_data and "scene.camera" in relayout_data:
        camera = relayout_data["scene.camera"]
        BASE_PLOTTER.change_camera_view(figure, camera)

    return figure


def load_dimensions(dimensions_json):
    try:
        dimensions = json.loads(dimensions_json)
    except:
        dimensions = BASE_DIMENSIONS
    return dimensions


poses = deepcopy(HEXAPOD_POSE)


def make_pose(alpha, beta, gamma):

    for k, _ in poses.items():
        poses[k] = {
            "id": k,
            "name": NAMES_LEG[k],
            "coxia": alpha,
            "femur": beta,
            "tibia": gamma,
        }
    return poses


def make_monospace(text):
    return dcc.Markdown(f" ```{text}")



def make_poses_message(poses):
    message = f"""
+----------------+------------+------------+------------+
| leg name       | coxia      | femur      | tibia      |
+----------------+------------+------------+------------+"""
    for pose in poses.values():
        message += f"""
| {pose['name']:14} | {pose['coxia']:<+10.2f} | {pose['femur']:<+10.2f} | {pose['tibia']:<+10.2f} |"""

    message += "\n+----------------+------------+------------+------------+"
    return make_monospace(message)


def make_alert_message(alert):
    return make_monospace(f"""
❗❗❗ALERT❗❗❗
⚠️ {alert} 🔴""")
