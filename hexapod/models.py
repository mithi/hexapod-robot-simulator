# This module contains the model of a hexapod
# It's used to manipulate the pose of the hexapod
from copy import deepcopy
from pprint import pprint
from math import atan2, degrees, isclose
import json
import numpy as np
from settings import PRINT_MODEL_ON_UPDATE, ALPHA_MAX_ANGLE, BETA_MAX_ANGLE, GAMMA_MAX_ANGLE
from hexapod.linkage import Linkage
import hexapod.ground_contact_solver.ground_contact_solver as gc
import hexapod.ground_contact_solver.ground_contact_solver2 as gc2

from hexapod.templates.pose_template import HEXAPOD_POSE
from hexapod.points import (
    Vector,
    frame_to_align_vector_a_to_b,
    frame_rotxyz,
    rotz,
)


# Dimensions f, s, and m
#
#       |-f-|
#       *---*---*--------
#      /    |    \     |
#     /     |     \    s
#    /      |      \   |
#   *------cog------* ---
#    \      |      /|
#     \     |     / |
#      \    |    /  |
#       *---*---*   |
#           |       |
#           |---m---|
#
#    y axis
#    ^
#    |
#    |
#    ----> x axis
#  cog (origin)
#
#
# Relative x-axis, for each attached linkage
#
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
#
class Hexagon:
    VERTEX_NAMES = (
        "right-middle",
        "right-front",
        "left-front",
        "left-middle",
        "left-back",
        "right-back",
    )
    COXIA_AXES = (0, 45, 135, 180, 225, 315)
    __slots__ = ("f", "m", "s", "cog", "head", "vertices", "all_points")

    def __init__(self, f, m, s):
        self.f = f
        self.m = m
        self.s = s

        self.cog = Vector(0, 0, 0, name="center-of-gravity")
        self.head = Vector(0, s, 0, name="head")
        self.vertices = [
            Vector(m, 0, 0, name=Hexagon.VERTEX_NAMES[0]),
            Vector(f, s, 0, name=Hexagon.VERTEX_NAMES[1]),
            Vector(-f, s, 0, name=Hexagon.VERTEX_NAMES[2]),
            Vector(-m, 0, 0, name=Hexagon.VERTEX_NAMES[3]),
            Vector(-f, -s, 0, name=Hexagon.VERTEX_NAMES[4]),
            Vector(f, -s, 0, name=Hexagon.VERTEX_NAMES[5]),
        ]

        self.all_points = self.vertices + [self.cog, self.head]


# ..........................................
# The hexapod model
# ..........................................
class VirtualHexapod:
    LEG_COUNT = 6
    __slots__ = (
        "body",
        "legs",
        "dimensions",
        "coxia",
        "femur",
        "tibia",
        "front",
        "side",
        "mid",
        "body_rotation_frame",
        "ground_contacts",
        "x_axis",
        "y_axis",
        "z_axis",
    )

    def __init__(self, dimensions):
        self._store_attributes(dimensions)
        self._init_legs()
        self._init_local_frame()

    def update(self, poses, assume_ground_targets=True):
        might_raise_poses_range_error(poses)

        self.body_rotation_frame = None
        might_twist = find_if_might_twist(self, poses)
        old_contacts = deepcopy(self.ground_contacts)

        # Update leg poses
        for pose in poses.values():
            i = pose["id"]
            self.legs[i].change_pose(pose["coxia"], pose["femur"], pose["tibia"])

        # Find new orientation of the body (new normal)
        # distance of cog from ground and which legs are on the ground
        if assume_ground_targets:
            # We are positive that our assumed target ground contact points
            # are correct then we don't have to test all possible cases
            legs, n_axis, height = gc.compute_orientation_properties(self.legs)
        else:
            legs, n_axis, height = gc2.compute_orientation_properties(self.legs)

        if n_axis is None:
            raise Exception("❗Pose Unstable. COG not inside support polygon.")

        # Tilt and shift the hexapod based on new normal
        frame = frame_to_align_vector_a_to_b(n_axis, Vector(0, 0, 1))
        self.rotate_and_shift(frame, height)
        self._update_local_frame(frame)

        # Twist around the new normal if you have to
        self.ground_contacts = [leg.ground_contact() for leg in legs]

        if might_twist:
            twist_frame = find_twist_frame(old_contacts, self.ground_contacts)
            self.rotate_and_shift(twist_frame)

        might_print_hexapod(self, poses)

    def detach_body_rotate_and_translate(self, rx, ry, rz, tx, ty, tz):
        # Detach the body of the hexapod from the legs
        # then rotate and translate body as if a separate entity
        frame = frame_rotxyz(rx, ry, rz)
        self.body_rotation_frame = frame

        for point in self.body.all_points:
            point.update_point_wrt(frame)
            point.move_xyz(tx, ty, tz)

        self._update_local_frame(frame)

    def move_xyz(self, tx, ty, tz):
        for point in self.body.all_points:
            point.move_xyz(tx, ty, tz)

        for leg in self.legs:
            for point in leg.all_points:
                point.move_xyz(tx, ty, tz)

    def update_stance(self, hip_stance, leg_stance):
        pose = deepcopy(HEXAPOD_POSE)
        pose[1]["coxia"] = -hip_stance  # right_front
        pose[2]["coxia"] = hip_stance  # left_front
        pose[4]["coxia"] = -hip_stance  # left_back
        pose[5]["coxia"] = hip_stance  # right_back

        for leg in pose.values():
            leg["femur"] = leg_stance
            leg["tibia"] = -leg_stance

        self.update(pose)

    def sum_of_dimensions(self):
        f, m, s = self.front, self.mid, self.side
        a, b, c = self.coxia, self.femur, self.tibia
        return f + m + s + a + b + c

    def _store_attributes(self, dimensions):
        self.body_rotation_frame = None
        self.dimensions = dimensions
        self.coxia = dimensions["coxia"]
        self.femur = dimensions["femur"]
        self.tibia = dimensions["tibia"]
        self.front = dimensions["front"]
        self.mid = dimensions["middle"]
        self.side = dimensions["side"]
        self.body = Hexagon(self.front, self.mid, self.side)

    def _init_legs(self):
        self.legs = []
        for i in range(VirtualHexapod.LEG_COUNT):
            linkage = Linkage(
                self.coxia,
                self.femur,
                self.tibia,
                coxia_axis=Hexagon.COXIA_AXES[i],
                new_origin=self.body.vertices[i],
                name=Hexagon.VERTEX_NAMES[i],
                id_number=i,
            )
            self.legs.append(linkage)

        self.ground_contacts = [leg.ground_contact() for leg in self.legs]

    def rotate_and_shift(self, frame, height=0):
        for vertex in self.body.all_points:
            vertex.update_point_wrt(frame, height)

        for leg in self.legs:
            leg.update_leg_wrt(frame, height)

    def _init_local_frame(self):
        self.x_axis = Vector(1, 0, 0, name="hexapod x axis")
        self.y_axis = Vector(0, 1, 0, name="hexapod y axis")
        self.z_axis = Vector(0, 0, 1, name="hexapod z axis")

    def _update_local_frame(self, frame):
        # Update the x, y, z axis centered at cog of hexapod
        self.x_axis.update_point_wrt(frame)
        self.y_axis.update_point_wrt(frame)
        self.z_axis.update_point_wrt(frame)


# ..........................................
# Helper functions
# ..........................................

def might_raise_poses_range_error(poses):
    angle_limits = {
        "coxia": ALPHA_MAX_ANGLE,
        "femur": BETA_MAX_ANGLE,
        "tibia": GAMMA_MAX_ANGLE,
    }

    def _within_range(angle, max_angle):
        return -max_angle <= angle <= max_angle

    def _raise_range_error(leg_name, joint_name, angle, max_angle):
        identifier = f"{leg_name} leg's {joint_name} angle is {angle}"
        msg = f"{identifier}. Must be within [-{max_angle}, {max_angle}]"
        raise Exception(msg)

    for pose in poses.values():
        for joint_name in angle_limits:

            angle = pose[joint_name]
            max_angle = angle_limits[joint_name]

            if _within_range(angle, max_angle):
                continue

            _raise_range_error(pose["name"], joint_name, angle, max_angle)


def get_hip_angle(leg_id, poses):
    if leg_id in poses:
        return poses[leg_id]["coxia"]

    if str(leg_id) in poses:
        return poses[str(leg_id)]["coxia"]

    # ❗Error will silently pass, is this ok?
    return 0.0


def find_if_might_twist(hexapod, poses):
    # The hexapod will only definitely NOT twist
    # if only two of the legs that's currently on the ground
    # has twisted its hips/coxia
    # i.e. only 2 legs with ground contact points have changed their alpha angles
    # i.e. we don't care if the legs which are not on the ground twisted its hips
    def _find_leg_id(leg_point):
        right_or_left, front_mid_or_back, _ = leg_point.name.split("-")
        leg_placement = right_or_left + "-" + front_mid_or_back
        return Hexagon.VERTEX_NAMES.index(leg_placement)

    did_change_count = 0

    for leg_point in hexapod.ground_contacts:
        leg_id = _find_leg_id(leg_point)
        old_hip_angle = hexapod.legs[leg_id].coxia_angle()
        new_hip_angle = get_hip_angle(leg_id, poses)
        if not isclose(old_hip_angle, new_hip_angle):
            did_change_count += 1
            if did_change_count >= 3:
                return True

    return False


def find_twist_frame(old_ground_contacts, new_ground_contacts):
    # This is the frame used to twist the model about the z axis

    def _make_contact_dict(contact_list):
        return {leg_point.name: leg_point for leg_point in contact_list}

    def _twist(v1, v2):
        # https://www.euclideanspace.com/maths/algebra/vectors/angleBetween/
        theta = atan2(v2.y, v2.x) - atan2(v1.y, v1.x)
        return rotz(degrees(theta))

    # Make dictionary mapping contact point name and leg_contact_point
    old_contacts = _make_contact_dict(old_ground_contacts)
    new_contacts = _make_contact_dict(new_ground_contacts)

    # Find at least one point that's the same
    same_point_name = None
    for key in old_contacts:
        if key in new_contacts:
            same_point_name = key
            break

    # We don't know how to rotate if we don't
    # know at least one point that's on the ground
    # before and after the movement,
    # so we assume that the hexapod didn't move
    if same_point_name is None:
        return np.eye(4)

    old = old_contacts[same_point_name]
    new = new_contacts[same_point_name]

    # Get the projection of these points in the ground
    old_vector = Vector(old.x, old.y, 0)
    new_vector = Vector(new.x, new.y, 0)

    twist_frame = _twist(new_vector, old_vector)

    # ❗IMPORTANT: We are assuming that because the point
    # is on the ground before and after
    # They should be at the same point after movement
    # I can't think of a case that contradicts this as of this moment
    return twist_frame


def might_print_hexapod(hexapod, poses):
    if not PRINT_MODEL_ON_UPDATE:
        return

    print("█████████████████████████████")
    print("█ start: Hexapod Model      █")
    print("█████████████████████████████")

    print("............")
    print("...Dimensions")
    print("............")
    print(json.dumps(hexapod.dimensions, indent=4))

    print("............")
    print("...Vertices")
    print("............")
    pprint(hexapod.body.all_points)

    print("............")
    print("...Legs")
    print("............")
    for i, leg in enumerate(hexapod.legs):
        print(f"\nleg{i}_points = ")
        pprint(leg.all_points)

    print("............")
    print("...Poses")
    print("............")
    print(json.dumps(poses, indent=4))

    print("█████████████████████████████")
    print("█ end: Hexapod Model        █")
    print("█████████████████████████████")
