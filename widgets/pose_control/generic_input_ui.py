from widgets.pose_control.joint_widget_maker import (
    make_all_joint_widgets,
    make_number_widget,
)
from widgets.pose_control.kinematics_section_maker import make_section

# ................................
# COMPONENTS
# ................................

widgets = make_all_joint_widgets(joint_input_function=make_number_widget)
KINEMATICS_WIDGETS_SECTION = make_section(widgets, add_joint_names=True)
