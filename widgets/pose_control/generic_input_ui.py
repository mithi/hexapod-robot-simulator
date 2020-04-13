from widgets.pose_control.joint_input_maker import (
    make_all_joint_inputs,
    make_joint_number_input,
)
from widgets.pose_control.kinematics_section_maker import make_section_pose_control

joint_inputs = make_all_joint_inputs(joint_input_function=make_joint_number_input)
SECTION_POSE_CONTROL = make_section_pose_control(joint_inputs, add_joint_names=True)
