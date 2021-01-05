from copy import deepcopy
import json
import dash_core_components as dcc
from hexapod.const import (
    BASE_PLOTTER,
    BASE_POSE,
    BASE_IK_PARAMS,
    BASE_DIMENSIONS,
    NAMES_LEG,
)

NEW_POSES = deepcopy(BASE_POSE)
POSES_MSG_HEADER = """
+----------------+------------+------------+------------+
| leg name       | coxia      | femur      | tibia      |
+----------------+------------+------------+------------+"""
POSES_MSG_LAST_ROW = "\n+----------------+------------+------------+------------+"


def make_pose(alpha, beta, gamma, poses=NEW_POSES):

    for k in poses.keys():
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


def load_params(params_json, params_type):
    try:
        params = json.loads(params_json)
    except Exception as e:
        print(f"Error loading json of type {params_type}. {e} | {params_json}")

        if params_type == "dims":
            return BASE_DIMENSIONS
        if params_type == "pose":
            return BASE_POSE
        if params_type == "ik":
            return BASE_IK_PARAMS

        raise Exception(
            f'params_type must be "dims", "pose" or "ik", not {params_type}'
        ) from e

    return params


def make_monospace(text):
    return dcc.Markdown(f" ```{text}")


def make_poses_message(poses):
    message = POSES_MSG_HEADER

    for pose in poses.values():
        name = pose["name"]
        coxia = pose["coxia"]
        femur = pose["femur"]
        tibia = pose["tibia"]
        row = f"\n| {name:14} | {coxia:<+10.2f} | {femur:<+10.2f} | {tibia:<+10.2f} |"
        message += row

    return make_monospace(message + POSES_MSG_LAST_ROW)


def make_alert_message(alert):
    return make_monospace(f"❗❗❗ALERT❗❗❗\n⚠️ {alert} 🔴")
