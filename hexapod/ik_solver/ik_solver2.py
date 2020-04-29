# Please look at the discussion of the Inverse Kinematics algorithm
# As detailed in the README of this directory
from copy import deepcopy
import numpy as np
from settings import ASSERTION_ENABLED, ALPHA_MAX_ANGLE
from hexapod.ik_solver.helpers import (
    BODY_ON_GROUND_ALERT_MSG,
    COXIA_ON_GROUND_ALERT_MSG,
    cant_reach_alert_msg,
    body_contact_shoved_on_ground,
    legs_too_short,
    beta_gamma_not_in_range,
    angle_above_limit,
    might_sanity_leg_lengths_check,
    might_sanity_beta_gamma_check,
    might_print_ik,
    might_print_points,
)
from hexapod.points import (
    Vector,
    length,
    add_vectors,
    scalar_multiply,
    vector_from_to,
    get_unit_vector,
    is_triangle,
    project_vector_onto_plane,
    angle_between,
    angle_opposite_of_last_side,
)
from hexapod.ik_solver.shared import (
    update_hexapod_points,
    find_twist_frame,
    compute_twist_wrt_to_world,
)
from hexapod.const import HEXAPOD_POSE

# This function inverse_kinematics_update()
# computes the joint angles required to
# rotate and translate the hexapod given the parameters
# - rot_x, rot_y, rot_z are how the hexapod should be rotated
# - percent_x, percent_y, percent_z are the shifts of the
# center of gravity of the hexapod
#
# The final points of contact by the hexapod and the ground
# are the same as the ground contacts right
# after doing the leg stance and hip stance
# unless the leg can't reach it.
#
# ❗❗❗IMPORTANT: The hexapod will be MODIFIED and returned along with
# a dictionary of POSES containing the 18 computed angles
# if the pose is impossible, this function will raise an error


def inverse_kinematics_update(hexapod, ik_parameters):
    return IKSolver(hexapod, ik_parameters).pose_and_hexapod()


class IKSolver:
    __slots__ = [
        "hexapod",
        "params",
        "poses",
        "leg_x_axis",
        "p0",
        "p1",
        "p2",
        "p3",
        "points",
        "body_to_foot_vector",
        "coxia_vector",
        "unit_coxia_vector",
        "coxia_to_foot_vector2d",
        "d",
        "alpha",
        "beta",
        "gamma",
        "leg_name",
        "legs_up_in_the_air",
        "body_contact",
        "foot_tip",
        "twist_frame",
    ]

    def __init__(self, hexapod, ik_parameters):
        self.hexapod = hexapod
        self.params = ik_parameters
        self.leg_x_axis = Vector(1, 0, 0)
        self.update_body_and_ground_contact_points()
        self.poses = deepcopy(HEXAPOD_POSE)

        self.legs_up_in_the_air = []
        for i in range(hexapod.LEG_COUNT):
            self.store_known_points(i)
            self.store_initial_vectors()
            self.compute_local_p0_p1_p3()
            self.compute_beta_gamma_local_p2()
            self.compute_alpha_and_twist_frame(i)
            self.points = [self.p0, self.p1, self.p2, self.p3]
            # Update point wrt world frame
            self.update_to_global_points()
            # Update hexapod's points to what we computed
            update_hexapod_points(self.hexapod, i, self.points)
            # Final p1, p2, p3, beta and gamma computed at this point
            self.poses[i]["coxia"] = self.alpha
            self.poses[i]["femur"] = self.beta
            self.poses[i]["tibia"] = self.gamma

        might_print_ik(self.poses, self.params, self.hexapod)

    def pose_and_hexapod(self):
        return self.poses, self.hexapod

    def update_body_and_ground_contact_points(self):
        tx = self.params["percent_x"] * self.hexapod.mid
        ty = self.params["percent_y"] * self.hexapod.side
        tz = self.params["percent_z"] * self.hexapod.tibia
        rotx, roty, rotz = (
            self.params["rot_x"],
            self.params["rot_y"],
            self.params["rot_z"],
        )

        self.hexapod.update_stance(self.params["hip_stance"], self.params["leg_stance"])
        self.hexapod.detach_body_rotate_and_translate(rotx, roty, rotz, tx, ty, tz)

        if body_contact_shoved_on_ground(self.hexapod):
            raise Exception(BODY_ON_GROUND_ALERT_MSG)

    def store_known_points(self, i):
        self.leg_name = self.hexapod.legs[i].name
        self.body_contact = self.hexapod.body.vertices[i]
        self.foot_tip = self.hexapod.legs[i].foot_tip()

    def store_initial_vectors(self):
        self.body_to_foot_vector = vector_from_to(self.body_contact, self.foot_tip)

        # find the coxia vector which is the vector
        # from body contact point to joint between coxia and femur limb
        projection = project_vector_onto_plane(
            self.body_to_foot_vector, self.hexapod.z_axis
        )
        self.unit_coxia_vector = get_unit_vector(projection)
        self.coxia_vector = scalar_multiply(self.unit_coxia_vector, self.hexapod.coxia)

        # coxia point / joint is the point connecting the coxia and tibia limbs
        coxia_point = add_vectors(self.body_contact, self.coxia_vector)
        if coxia_point.z < self.foot_tip.z:
            raise Exception(COXIA_ON_GROUND_ALERT_MSG)

    def compute_local_p0_p1_p3(self):
        self.p0 = Vector(0, 0, 0)
        self.p1 = Vector(self.hexapod.coxia, 0, 0)

        # Find p3 aka foot tip (ground contact) with respect to the local leg frame
        rho = angle_between(self.unit_coxia_vector, self.body_to_foot_vector)
        body_to_foot_length = length(self.body_to_foot_vector)
        p3x = body_to_foot_length * np.cos(np.radians(rho))
        p3z = -body_to_foot_length * np.sin(np.radians(rho))
        self.p3 = Vector(p3x, 0, p3z)

    def compute_beta_gamma_local_p2(self):
        # These values are needed to compute
        # p2 aka tibia joint (point between femur limb and tibia limb)
        self.coxia_to_foot_vector2d = vector_from_to(self.p1, self.p3)
        self.d = length(self.coxia_to_foot_vector2d)

        # If we can form this triangle
        # # this means we probably can reach the target ground contact point
        if is_triangle(self.hexapod.tibia, self.hexapod.femur, self.d):
            # CASE A: a triangle can be formed with
            # coxia to foot vector, hexapod's femur and tibia
            self.compute_when_triangle_can_form()
        else:
            # CASE B: It's impossible to reach target ground point
            self.compute_when_triangle_cannot_form()

        not_within_range, alert_msg = beta_gamma_not_in_range(
            self.beta, self.gamma, self.leg_name
        )
        if not_within_range:
            raise Exception(alert_msg)

    def compute_when_triangle_can_form(self):
        theta = angle_opposite_of_last_side(
            self.d, self.hexapod.femur, self.hexapod.tibia
        )
        phi = angle_between(self.coxia_to_foot_vector2d, self.leg_x_axis)

        self.beta = theta - phi  # case 1 or 2
        if self.p3.z > 0:  # case 3
            self.beta = theta + phi

        z_ = self.hexapod.femur * np.sin(np.radians(self.beta))
        x_ = self.p1.x + self.hexapod.femur * np.cos(np.radians(self.beta))

        self.p2 = Vector(x_, 0, z_)
        femur_vector = vector_from_to(self.p1, self.p2)
        tibia_vector = vector_from_to(self.p2, self.p3)
        self.gamma = 90 - angle_between(femur_vector, tibia_vector)

        if self.p2.z < self.p3.z:
            raise Exception(cant_reach_alert_msg(self.leg_name, "blocking"))

    def might_raise_cant_reach_target(self):
        if self.d + self.hexapod.tibia < self.hexapod.femur:
            raise Exception(cant_reach_alert_msg(self.leg_name, "femur"))
        if self.d + self.hexapod.femur < self.hexapod.tibia:
            raise Exception(cant_reach_alert_msg(self.leg_name, "tibia"))

        # Then hexapod.femur + hexapod.tibia < d:
        self.legs_up_in_the_air.append(self.leg_name)
        LEGS_TOO_SHORT, alert_msg = legs_too_short(self.legs_up_in_the_air)
        if LEGS_TOO_SHORT:
            raise Exception(alert_msg)

    def only_few_legs_cant_reach_target(self):
        # Try to reach it by making the legs stretch
        # i.e. p1, p2, p3 are all on the same line
        femur_tibia_direction = get_unit_vector(self.coxia_to_foot_vector2d)
        femur_vector = scalar_multiply(femur_tibia_direction, self.hexapod.femur)
        self.p2 = add_vectors(self.p1, femur_vector)
        tibia_vector = scalar_multiply(femur_tibia_direction, self.hexapod.tibia)
        self.p3 = add_vectors(self.p2, tibia_vector)

        # Find beta and gamma
        self.gamma = 0.0
        self.beta = angle_between(self.leg_x_axis, femur_vector)
        if femur_vector.z < 0:
            self.beta = -self.beta

    def compute_when_triangle_cannot_form(self):
        self.might_raise_cant_reach_target()
        self.only_few_legs_cant_reach_target()

    def compute_alpha_and_twist_frame(self, i):

        alpha, twist_frame = find_twist_frame(self.hexapod, self.unit_coxia_vector)
        alpha = compute_twist_wrt_to_world(alpha, self.hexapod.body.COXIA_AXES[i])

        limit, msg = angle_above_limit(
            alpha, ALPHA_MAX_ANGLE, self.leg_name, "(alpha/coxia)"
        )
        if limit:
            raise Exception(msg)

        self.alpha = alpha
        self.twist_frame = twist_frame

    def update_to_global_points(self):
        might_print_points(self.points, self.leg_name)

        # Convert points from local leg coordinate frame to world coordinate frame
        for point in self.points:
            point.update_point_wrt(self.twist_frame)
            if ASSERTION_ENABLED:
                assert (
                    self.hexapod.body_rotation_frame is not None
                ), "No rotation frame!"
            point.update_point_wrt(self.hexapod.body_rotation_frame)
            point.move_xyz(
                self.body_contact.x, self.body_contact.y, self.body_contact.z
            )

        might_sanity_leg_lengths_check(self.hexapod, self.leg_name, self.points)
        might_sanity_beta_gamma_check(self.beta, self.gamma, self.leg_name, self.points)
