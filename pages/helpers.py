import dash_core_components as dcc
from hexapod.const import BASE_PLOTTER
from hexapod.const import HEXAPOD_POSE, NAMES_LEG, BASE_DIMENSIONS
from copy import deepcopy
import json


poses = deepcopy(HEXAPOD_POSE)
poses_mgs_header = f"""
+----------------+------------+------------+------------+
| leg name       | coxia      | femur      | tibia      |
+----------------+------------+------------+------------+"""
poses_msg_last_row = "\n+----------------+------------+------------+------------+"


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


def change_camera_view(figure, relayout_data):
    if relayout_data and "scene.camera" in relayout_data:
        camera = relayout_data["scene.camera"]
        BASE_PLOTTER.change_camera_view(figure, camera)

    return figure


def load_dimensions(dimensions_json):
    try:
        dimensions = json.loads(dimensions_json)
    except Exception as e:
        print(f"Error loading dimension_json. {e} | {dimensions_json}")
        dimensions = BASE_DIMENSIONS
    return dimensions


def make_monospace(text):
    return dcc.Markdown(f" ```{text}")


def make_poses_message(poses):
    message = poses_mgs_header

    for pose in poses.values():
        name = pose["name"]
        coxia = pose["coxia"]
        femur = pose["femur"]
        tibia = pose["tibia"]
        row = f"\n| {name:14} | {coxia:<+10.2f} | {femur:<+10.2f} | {tibia:<+10.2f} |"
        message += row

    return make_monospace(message + poses_msg_last_row)


def make_alert_message(alert):
    return make_monospace(f"❗❗❗ALERT❗❗❗\n⚠️ {alert} 🔴")
