# hexapod-robot-simulator
- Hexapod robot simulator using Plotly Dash
- Still a work in progress

# Requirements
- Python 3
- Plotly 4
- Plotly Dash
- Numpy

# Run
```
$ python index.py
```
# Notes 
**KNOWN ISSUE**
  - Leg can criss-cross each other which shouldn't be the case, I'm open to hearing ideas on how to go about this

 **Predefined Poses**
  - You can hardcode and save predefined poses in
```
. /hexapod/templates/pose_template.py
```
  - It will show as a radio button you can select at the test page
```
  ./pages/page_test.py
```
**Selecting user interface preferences**
- You can also select if you like to tweak poses via sliders, knobs or
text fireld. You can do thisby commenting out the other options in lines `12-15` of
```
./pages/page_kinematics.py

#from widgets.pose_control.generic_slider_ui import SECTION_POSE_CONTROL
from widgets.pose_control.generic_input_ui import SECTION_POSE_CONTROL
#from widgets.pose_control.generic_knob_ui import SECTION_POSE_CONTROL
#from widgets.pose_control.generic_daq_slider_ui import SECTION_POSE_CONTROL
```

# Screenshots
| ![](./img/screen_shot-v1-4.png) | ![](./img/screen_shot-v1-2.png) |
| ------------- |:-------------:|
| ![](./img/screen_shot-v1-3.png) | ![](./img/screen_shot-v1-1.png) |
