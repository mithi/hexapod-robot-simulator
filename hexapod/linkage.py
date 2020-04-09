# -------------
# LINKAGE
# -------------
# Neutral position of the linkages (alpha=0, beta=0, gamma=0)
# note that at neutral position:
#  link b and link c are perpendicular to each other
#  link a and link b form a straight line
#  link a coincide with x axis
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
    get_unit_normal,
    is_point_inside_triangle,
    frame_yrotate_xtranslate,
    frame_zrotate_xytranslate,
)


class Linkage:
    POINT_NAMES = ["coxia", "femur", "tibia"]

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
        self.store_linkage_attributes(a, b, c, coxia_axis, new_origin, name, id_number)
        self.save_new_pose(alpha, beta, gamma)

    def all_points(self):
        return [self.p0, self.p1, self.p2, self.p3]

    def coxia_angle(self):
        return self._alpha

    def coxia_point(self):
        return self.p1

    def femur_point(self):
        return self.p2

    def foot_tip(self):
        return self.p3

    def ground_contact(self):
        return self.ground_contact_point

    def store_linkage_attributes(
        self, a, b, c, coxia_axis, new_origin, name, id_number
    ):
        self._a = a
        self._b = b
        self._c = c
        self._new_origin = new_origin
        self._coxia_axis = coxia_axis
        self.id = id_number
        self.name = name

    def save_new_pose(self, alpha, beta, gamma):
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma

        # frame_ab is the pose of frame_b wrt frame_a
        frame_01 = frame_yrotate_xtranslate(theta=-self._beta, x=self._a)
        frame_12 = frame_yrotate_xtranslate(theta=90 - self._gamma, x=self._b)
        frame_23 = frame_yrotate_xtranslate(theta=0, x=self._c)

        frame_02 = np.matmul(frame_01, frame_12)
        frame_03 = np.matmul(frame_02, frame_23)
        new_frame = frame_zrotate_xytranslate(
            self._coxia_axis + self._alpha, self._new_origin.x, self._new_origin.y
        )

        # find points wrt to body contact point
        p0 = Point(0, 0, 0)
        p1 = p0.get_point_wrt(frame_01)
        p2 = p0.get_point_wrt(frame_02)
        p3 = p0.get_point_wrt(frame_03)

        # find points wrt to center of gravity
        self.p0 = deepcopy(self._new_origin)
        self.p0.name += "-body-contact"
        self.p1 = p1.get_point_wrt(new_frame, name=self.name + "-coxia")
        self.p2 = p2.get_point_wrt(new_frame, name=self.name + "-femur")
        self.p3 = p3.get_point_wrt(new_frame, name=self.name + "-tibia")

        self.ground_contact_point = self.compute_ground_contact()

    def change_pose(self, alpha=None, beta=None, gamma=None):
        alpha = alpha or self._alpha
        beta = beta or self._beta
        gamma = gamma or self._gamma
        self.save_new_pose(alpha, beta, gamma)

    def update_leg_wrt(self, frame, height):
        self.p0.update_point_wrt(frame, height)
        self.p1.update_point_wrt(frame, height)
        self.p2.update_point_wrt(frame, height)
        self.p3.update_point_wrt(frame, height)

    def compute_ground_contact(self):
        if self._tip_wrt_cog() <= 0:
            if self._femur_wrt_cog() <= 0:
                return self.coxia_point()
            else:
                return self.femur_point()

        if self._tip_wrt_cog() >= self._femur_wrt_cog():
            return self.foot_tip()
        else:
            return self.femur_point()

    def _tip_wrt_cog(self):
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
        return -self.foot_tip().z

    def _femur_wrt_cog(self):
        return -self.femur_point().z
