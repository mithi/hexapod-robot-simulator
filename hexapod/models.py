# The module contains the model of a hexapod
# Use it to manipulate the pose of the hexapod
import numpy as np
from copy import deepcopy
import json
from settings import PRINT_MODEL_ON_UPDATE, PRINT_MODEL_POSE_ON_UPDATE
from .linkage import Linkage
from .ground_contact_solver import get_legs_on_ground
from .templates.pose_template import HEXAPOD_POSE
from .points import (
    Point,
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
    VERTEX_NAMES = [
        "right-middle",
        "right-front",
        "left-front",
        "left-middle",
        "left-back",
        "right-back",
    ]
    COXIA_AXES = [0, 45, 135, 180, 225, 315]

    def __init__(self, f, m, s):
        self.f = f
        self.m = m
        self.s = s

        self.cog = Point(0, 0, 0, name="center of gravity")
        self.head = Point(0, s, 0, name="head")
        self.vertices = [
            Point(m, 0, 0, name=Hexagon.VERTEX_NAMES[0]),
            Point(f, s, 0, name=Hexagon.VERTEX_NAMES[1]),
            Point(-f, s, 0, name=Hexagon.VERTEX_NAMES[2]),
            Point(-m, 0, 0, name=Hexagon.VERTEX_NAMES[3]),
            Point(-f, -s, 0, name=Hexagon.VERTEX_NAMES[4]),
            Point(f, -s, 0, name=Hexagon.VERTEX_NAMES[5]),
        ]

        self.all_points = self.vertices + [self.cog, self.head]


class VirtualHexapod:
    LEG_COUNT = 6

    def __init__(self, dimensions=None):
        self._store_attributes(dimensions)
        self._init_legs()
        self._init_local_frame()

    def print(self):
        print_hexapod(self)

    def update(self, poses):
        self.body_rotation_frame = None
        might_twist = find_if_might_twist(self, poses)
        old_contacts = deepcopy(self.ground_contacts)

        # Update leg poses
        for _, pose in poses.items():
            i = pose["id"]
            self.legs[i].change_pose(pose["coxia"], pose["femur"], pose["tibia"])

        # Find new orientation of the body, height, and which legs are on the ground
        legs, self.n_axis, height = get_legs_on_ground(self.legs)

        if self.n_axis is None:
            raise Exception("❗❗❗Pose Unstable. COG not inside support polygon")

        # Tilt and shift the hexapod based on new normal
        frame = frame_to_align_vector_a_to_b(self.n_axis, Point(0, 0, 1))
        self.rotate_and_shift(frame, height)
        self._update_local_frame(frame)

        # Twist around the new normal if you have to
        self.ground_contacts = [leg.ground_contact() for leg in legs]

        if might_twist:
            twist_frame = find_twist_frame(old_contacts, self.ground_contacts)
            self.rotate_and_shift(twist_frame)

        # Finally print result if you have to
        if PRINT_MODEL_POSE_ON_UPDATE:
            print(json.dumps(poses, indent=4))
        if PRINT_MODEL_ON_UPDATE:
            self.print()

    def detach_body_rotate_and_translate(self, rx, ry, rz, tx, ty, tz):
        # Detaches the body of the hexapod from the legs
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
        pose[1]["coxia"] = -hip_stance # right_front
        pose[2]["coxia"] = hip_stance # left_front
        pose[4]["coxia"] = -hip_stance # left_back
        pose[5]["coxia"] = hip_stance # right_back

        for key in pose.keys():
            pose[key]["femur"] = leg_stance
            pose[key]["tibia"] = -leg_stance

        self.update(pose)

    def _store_attributes(self, dimensions):
        self.body_rotation_frame = None
        self.dimensions = dimensions
        f = dimensions["front"]
        s = dimensions["side"]
        m = dimensions["middle"]
        a = dimensions["coxia"]
        b = dimensions["femur"]
        c = dimensions["tibia"]
        self.coxia = a
        self.femur = b
        self.tibia = c
        self.front = f
        self.mid = m
        self.side = s
        self.body = Hexagon(f, m, s)

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
        self.x_axis = Point(1, 0, 0, name="hexapod x axis")
        self.y_axis = Point(0, 1, 0, name="hexapod y axis")
        self.z_axis = Point(0, 0, 1, name="hexapod z axis")

    def _update_local_frame(self, frame):
        # Update the x, y, z axis centered at cog of hexapod
        self.x_axis.update_point_wrt(frame)
        self.y_axis.update_point_wrt(frame)
        self.z_axis.update_point_wrt(frame)


def get_hip_angle(leg_id, poses):
    try:
        return poses[leg_id]["coxia"]
    except KeyError:
        try:
            return poses[str(leg_id)]["coxia"]
        except KeyError:
            return 0
    return 0


def find_if_might_twist(hexapod, poses):
    # hexapod will only definitely NOT twist
    # if only two of the legs (currently on the ground)
    # has twisted its hips/coxia
    # i.e. only 2 legs with ground contact points have changed alpha angle
    # i.e. we don't care if the legs which are not on the ground twisted its hips
    def _find_leg_id(leg_point):
        right_or_left, front_mid_or_back, _ = leg_point.name.split("-")
        leg_placement = right_or_left + "-" + front_mid_or_back
        leg_id = Hexagon.VERTEX_NAMES.index(leg_placement)
        return leg_id

    did_change_count = 0

    for leg_point in hexapod.ground_contacts:
        leg_id = _find_leg_id(leg_point)
        old_hip_angle = hexapod.legs[leg_id].coxia_angle()
        new_hip_angle = get_hip_angle(leg_id, poses)
        if not np.isclose(old_hip_angle, new_hip_angle):
            did_change_count += 1
            if did_change_count >= 3:
                return True

    return False


def find_twist_frame(old_ground_contacts, new_ground_contacts):
    # This is the frame used to twist the model about the z axis

    def _make_contact_dict(contact_list):
        contact_dict = {}
        for leg_point in contact_list:
            name = leg_point.name
            contact_dict[name] = leg_point
        return contact_dict

    def _twist(v1, v2):
        # https://www.euclideanspace.com/maths/algebra/vectors/angleBetween/
        theta = np.arctan2(v2.y, v2.x) - np.arctan2(v1.y, v1.x)
        return rotz(np.degrees(theta))

    # Make dictionary mapping contact point name and leg_contact_point
    old_contacts = _make_contact_dict(old_ground_contacts)
    new_contacts = _make_contact_dict(new_ground_contacts)

    # Find at least one point that's the same
    same_point_name = None
    for key in old_contacts.keys():
        if key in new_contacts.keys():
            same_point_name = key
            break

    # We don't know how to rotate if we don't
    # know at least one point that's contacting the ground
    # before and after the movement
    # so we assume that the hexapod didn't move
    if same_point_name is None:
        return np.eye(4)

    old = old_contacts[same_point_name]
    new = new_contacts[same_point_name]

    # Get the projection of these points in the ground
    old_vector = Point(old.x, old.y, 0)
    new_vector = Point(new.x, new.y, 0)

    twist_frame = _twist(new_vector, old_vector)

    # ❗IMPORTANT: We are assuming that because the point
    # is on the ground before and after
    # They should be at the same point after movement
    # I can't think of a case that contradicts this as of this moment
    return twist_frame


def print_hexapod(hexapod):
    print("*********************")
    print("Hexapod Model")
    print("*********************")

    print("...Vertices")
    for point in hexapod.body.all_points:
        print("  ", point)

    print("...legs")

    for leg in hexapod.legs:
        for point in leg.all_points:
            print("  ", point)

    print("...dimensions")
    print(json.dumps(hexapod.dimensions, indent=4))
    print("*********************")
    print("End Hexapod Model")
    print("*********************")
