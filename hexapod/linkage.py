# -------------
# LINKAGE
# -------------
# Neutral position of the linkages (alpha=0, beta=0, gamma=0)
# note that at neutral position:
#  link b and link c are perpendicular to each other
#  link a and link b form a straight line
#  link a and the leg x axis are aligned
#
# alpha - the angle linkage a makes with x_axis about z axis
# beta - the angle that linkage a makes with linkage b
# gamma - the angle that linkage c make with the line perpendicular to linkage b
#
#
# MEASUREMENTS
#
#  |--- a--------|--b--|
#  |=============|=====| p2 -------
#  p0            p1    |          |
#                      |          |
#                      |          c
#                      |          |
#                      |          |
#                      | p3  ------
#
# p0 - body contact
# p1 - coxia point
# p2 - femur point
# p3 - foot tip
#
#  z axis
#  |
#  |
#  |------- x axis
# origin
#
#
# ANGLES beta and gamma
#                /
#               / beta
#         ---- /* ---------
#        /    //\\        \
#       b    //  \\        \
#      /    //    \\        c
#     /    //beta  \\        \
# *=======* ---->   \\        \
# |---a---|          \\        \
#                     *-----------
#
# |--a--|---b----|
# *=====*=========* -------------
#               | \\            \
#               |  \\            \
#               |   \\            c
#               |    \\            \
#               |gamma\\            \
#               |      *----------------
#

import numpy as np
from copy import deepcopy
from .points import (
    Point,
    frame_yrotate_xtranslate,
    frame_zrotate_xytranslate,
)


class Linkage:
    POINT_NAMES = ["coxia", "femur", "tibia"]
    __slots__ = [
        "a",
        "b",
        "c",
        "alpha",
        "beta",
        "gamma",
        "coxia_axis",
        "new_origin",
        "name",
        "id",
        "all_points",
        "ground_contact_point",
        "p0",
        "p1",
        "p2",
        "p3",
    ]

    def __init__(
        self,
        a,
        b,
        c,
        alpha=0,
        beta=0,
        gamma=0,
        coxia_axis=0,
        new_origin=Point(0, 0, 0),
        name=None,
        id_number=None,
    ):
        self.a = a
        self.b = b
        self.c = c
        self.new_origin = new_origin
        self.coxia_axis = coxia_axis
        self.id = id_number
        self.name = name
        self.change_pose(alpha, beta, gamma)

    def coxia_angle(self):
        return self.alpha

    def coxia_point(self):
        return self.p1

    def femur_point(self):
        return self.p2

    def foot_tip(self):
        return self.p3

    def ground_contact(self):
        return self.ground_contact_point

    def change_pose(self, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        # frame_ab is the pose of frame_b wrt frame_a
        frame_01 = frame_yrotate_xtranslate(theta=-self.beta, x=self.a)
        frame_12 = frame_yrotate_xtranslate(theta=90 - self.gamma, x=self.b)
        frame_23 = frame_yrotate_xtranslate(theta=0, x=self.c)

        frame_02 = np.matmul(frame_01, frame_12)
        frame_03 = np.matmul(frame_02, frame_23)
        new_frame = frame_zrotate_xytranslate(
            self.coxia_axis + self.alpha, self.new_origin.x, self.new_origin.y
        )

        # find points wrt to body contact point
        p0 = Point(0, 0, 0)
        p1 = p0.get_point_wrt(frame_01)
        p2 = p0.get_point_wrt(frame_02)
        p3 = p0.get_point_wrt(frame_03)

        # find points wrt to center of gravity
        self.p0 = deepcopy(self.new_origin)
        self.p0.name += "-body-contact"
        self.p1 = p1.get_point_wrt(new_frame, name=self.name + "-coxia")
        self.p2 = p2.get_point_wrt(new_frame, name=self.name + "-femur")
        self.p3 = p3.get_point_wrt(new_frame, name=self.name + "-tibia")

        self.all_points = [self.p0, self.p1, self.p2, self.p3]
        self.ground_contact_point = self.compute_ground_contact()

    def update_leg_wrt(self, frame, height):
        for point in self.all_points:
            point.update_point_wrt(frame, height)

    def compute_ground_contact(self):
        # ❗IMPORTANT: Verify if this assumption is correct
        ground_contact = self.p3
        for point in reversed(self.all_points):
            if point.z < ground_contact.z:
                ground_contact = point

        return ground_contact

    def __repr__(self):
        leg_string = make_linkage_repr(self)
        leg_string += f"Points of {self.name} leg:\n"

        for point in self.all_points:
            leg_string += f"  {point}\n"

        leg_string += f"  ground contact: {self.ground_contact()}\n"
        return leg_string


def make_linkage_repr(leg):
    return f"""Linkage(
  a={leg.a},
  b={leg.b},
  c={leg.c},
  alpha={leg.alpha},
  beta={leg.beta},
  gamma={leg.gamma},
  new_axis={leg.coxia_axis},
  id_number={leg.id},
  name='{leg.name}',
  new_origin={leg.new_origin},
)

"""

#
#          /*
#         //\\
#        //  \\
#       //    \\
#      //      \\
# *===* ---->   \\ ---------
#                \\       |
#                 \\   tip height (positive)
#                  \\     |
#                   \\ -----
#
#
# *===*=======*
#           | \\
#           |  \\
# (positive)|   \\
#    tip height  \\
#           |     \\
#         ------    *----
#
#                *=========* -----
#               //             |
#              // (negative) tip height
#             //               |
# *===*=======*  -------------------
# Negative only if body contact point
# is touching the ground
