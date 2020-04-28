from widgets.pose_control.joint_widget_maker import (
    make_all_joint_widgets,
    make_daq_slider,
)
from widgets.pose_control.kinematics_section_maker import make_section

# ................................
# COMPONENTS
# ................................

widgets = make_all_joint_widgets(joint_input_function=make_daq_slider)
KINEMATICS_WIDGETS_SECTION = make_section(
    widgets, style_to_use={"padding": "0 0 0 3em"}
)
