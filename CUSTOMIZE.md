## Too slow?
Instead of `UPDATE_MODE='drag'`, set `UPDATE_MODE='mouseup'` in
```
./widgets/const.py
```
This will make widgets only start updating when you release the mouse button

## Debugging inverse kinematics
In the first line of
```
./pages/page-inverse.py
```
The inverse kinematics solver already updates the points of the hexapod
but if you want to test whether the pose is indeed correct
ie use the poses returned by the inverse kinematics solve
set `RECOMPUTE_HEXAPOD=true` otherwise for faster graph/plot updates, set `RECOMPUTE_HEXAPOD=False`
```
RECOMPUTE_HEXAPOD = False
```

## Debugging other things
If you look at lines `55-60` of
```
index.py
```
You will see
```
if __name__ == '__main__':
  app.run_server(
    debug=False,
    dev_tools_ui=False,
    dev_tools_props_check=False
  )
```
Set them all to `True`

## Setting the range of joint angles
Modify it in
```
./hexapod/MAX_ANGLES.py
```
They currently default to the following
```
ALPHA_MAX_ANGLE = 120
BETA_MAX_ANGLE = 120
GAMMA_MAX_ANGLE = 120
BODY_MAX_ANGLE = 60
LEG_STANCE_MAX_ANGLE = 90
HIP_STANCE_MAX_ANGLE = 45

# LEG STANCE
# would define the starting leg position used to compute
# the target ground contact for inverse kinematics poses
# femur/ beta = -leg_stance
# tibia/ gamma = leg_stance

# HIP STANCE
# would defined the starting hip position used to computer
# the target ground contact for inverse kinematics poses
# coxia/alpha angle of
#  right_front = -hip_stance
#   left_front = hip_stance
#    left_back = -hip_stance
#   right_back = hip_stance
#  left_middle = 0
# right_middle = 0
```

## Pose control user interface for kinematics page
You can also select if you like to tweak poses via sliders, knobs or
text field. You can do this by commenting out the other options in
 ```
 ./pages/page_kinematics.py
 ```
Check out lines `12-15` of this file
```
#from widgets.pose_control.generic_slider_ui import SECTION_POSE_CONTROL
from widgets.pose_control.generic_input_ui import SECTION_POSE_CONTROL
#from widgets.pose_control.generic_knob_ui import SECTION_POSE_CONTROL
#from widgets.pose_control.generic_daq_slider_ui import SECTION_POSE_CONTROL
```

# Disabled functionality
- This is no longer a feature of this app
- Predefining poses
You can hardcode and save predefined poses in
```
. /hexapod/templates/pose_template.py
```
You'll see
```
example_pose = {
  0: {"coxia": 16.61, "femur": 28.93 , "tibia": -33.95, "name": "right-middle", "id": 0},
  1: {"coxia": 23.46, "femur": 44.83, "tibia": -46.41, "name": "right-front", "id": 1},
  2: {"coxia": 29.53, "femur": 44.86, "tibia": -44.22, "name": "left-front", "id": 2},
  3: {"coxia": 28.19, "femur": 29.14, "tibia": -31.13 , "name": "left-middle", "id": 3},
  4: {"coxia": 29.73, "femur": 15.62, "tibia": -13.95, "name": "left-back", "id": 4},
  5: {"coxia": 20.00, "femur": 15.62, "tibia": -17.44 , "name": "right-back", "id": 5}
}

PREDEFINED_POSES = {
  'NONE': None,
  'neutral': HEXAPOD_POSE,
  'example-pose': example_pose,
}
```
When you include
```
widgets.radio_items_ui.section_predefined_pose_control in your layout
```
and add it on
```
INPUTS = SLIDERS_TEST_INPUTS + DIMENSION_INPUTS + [Input('camera-view-values', 'children')] + [Input( 'predefined-poses', 'value')]
@app.callback(
  Output('hexapod-plot', 'figure'),
  INPUTS,
  [State('hexapod-plot', 'figure')]
)
def update_hexapod_plot(alpha, beta, gamma, f, s, m, h, k, a, camera, figure):
```
It will show as a radio button you can select at the test page
```
  ./pages/page_test.py
```

