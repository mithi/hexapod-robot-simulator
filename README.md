# [☕](https://ko-fi.com/minimithi) [![Code Climate](https://codeclimate.com/github/mithi/hexapod-robot-simulator/badges/gpa.svg)](https://codeclimate.com/github/mithi/hexapod-robot-simulator) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) [![HitCount](https://hits.dwyl.com/mithi/hexapod-robot-simulator.svg)](https://hits.dwyl.com/mithi/hexapod-robot-simulator) [![Build Status](https://travis-ci.com/mithi/hexapod-robot-simulator.svg?branch=master)](https://travis-ci.com/github/mithi/hexapod-robot-simulator)

# 🕷️ Mithi's Hexapod Robot Simulator

- A bare minimum browser-based hexapod robot simulator built from first principles 🕷️
- If you like this project, consider [buying me a few ☕ cups of coffee](https://ko-fi.com/minimithi). 💕

|  |  |  |  |
|---------|---------|---------|---------|
|![Twisting turning and tilting](https://mithi.github.io/robotics-blog/robot-only-x1.gif)|<img src="https://mithi.github.io/robotics-blog/v2-hexapod-1.gif" width="550"/>|<img src="https://mithi.github.io/robotics-blog/v2-hexapod-2.gif" width="500"/>|![Adjusting camera view](https://mithi.github.io/robotics-blog/robot-only-x2.gif)|

| STATUS | FEATURE   | DESCRIPTION  |
|---|-----------|--------------|
| 🎉 | Forward Kinematics | Given angles of each joint, what does the robot look like?|
| 🎉 | Inverse Kinematics | What are the angles of each joint to make the robot look the way I want? Is it even possible? Why or why not? |
| 🎉 | Uniform Movements |  If all of the legs behaved the same way, how will the hexapod robot as a whole behave? |
| 🎉 | Customizability | Set the dimensions and shape of the robot's body and legs. (6 parameters) |
| 🎉 | Usability | Control the camera view, pan, tilt, zoom, whatever. |
| 🎉 | Simplicity | Minimal dependencies. Depends solely on Numpy for calculations. Uses only Plotly Dash for plotting, Dash can be safely replaced if a better 3d plotting library is available. |
| ❗ | Stability Check (WIP) | If we pose the robot in a particular way, will it fall over? |
| ❗ | Fast | Okay, it's not as fast as I wanted, but when run locally, it's okay |
| ❗ | Bug-free | Fine, right now there's still room for improvement |
| ❗ | Well-tested | Yeah, I need to compile test cases first |

## 🕷️ Preview

|![IK](https://mithi.github.io/robotics-blog/v2-ik-ui.gif)|![Kinematics](https://mithi.github.io/robotics-blog/v2-kinematics-ui.gif)|
|----|----|
| ![IK](https://mithi.github.io/robotics-blog/UI-1.gif) | ![Kinematics](https://mithi.github.io/robotics-blog/UI-2.gif) |

## 🕷️ Requirements

- [x] Python 3.8.1
- [x] Plotly Dash 1.10.0
- [x] Plotly Dash Daq 0.4.0
- [x] Numpy 1.18.1
- [x] See also [./requirements.txt](./requirements.txt)

## 🕷Run

```bash
$ python index.py
Running on http://127.0.0.1:8050/
```

- Modify default settings with [./settings.py](./settings.py)
- Dark Mode is the default - modify style settings with [./style_settings.py](./style_settings.py)

## 🕷️Conventions and Algorithms

- Definitions
  - [`Linkage`](./hexapod/linkage.py)
  - [`VirtualHexapod`](./hexapod/models.py#L238)
- [Inverse Kinematics Algorithm](./hexapod/ik_solver/README.md)
- [Finding ground contact points, tilt, and height of hexapod](./hexapod/ground_contact_solver.py#L45)
- [Transforming hexapod to step on correct target ground contacts](./hexapod/ik_solver/recompute_hexapod.py#L15)
- Determining if the Hexapod should twist
  - [`find_if_might_twist`](./hexapod/models.py#L228)
  - [`find_twist_frame`](./hexapod/models.py#L254)

## 🕷️ Notes

- ❗Now live on https://hexapod-robot-simulator.herokuapp.com ! **BUT** (and a big one) I highly suggest that you run it locally**. When run locally, it's pretty speedy! On the other hand, the link above is barely usable. Might convert this to to be a fully client-side Javascript app later, maybe?

- ❗This implementation uses matrices, **NOT** quaternions. I'm aware that quaternions is far superior in every single way. In the (un)forseeable future, maybe?

- ❗Frankly, [My IK algorithm](https://github.com/mithi/hexapod-robot-simulator/blob/master/hexapod/ik_solver/README.md) isn't all that great, it's just something I came up with based on what I remember back in college plus browsing through the [Mathematics Stack Exchange](https://math.stackexchange.com/). It might not be the best, but it's the most intuitive that I can think of. If you want something closer to the the state-of-the-art, maybe try [Unity's Fast IK](https://assetstore.unity.com/packages/tools/animation/fast-ik-139972) or [ROS IKFast](http://wiki.ros.org/Industrial/Tutorials/Create_a_Fast_IK_Solution).

- I believe that the idea that it's best to be kind to one another shouldn't be controversial. [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](https://www.contributor-covenant.org/)

## ⚠️ Known issues

- [ ] ❗[Priorities](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3APRIORITY)
- [ ] ❗[Help Wanted](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
- [ ] ❗[Bugs](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3Abug)
- [ ] ❗[All](https://github.com/mithi/hexapod-robot-simulator/issues)

## 🕷️ Screenshots

| ![Kinematics](https://mithi.github.io/robotics-blog/v2-kinematics-screenshot.png)|
|---|
| ![IK](https://mithi.github.io/robotics-blog/v2-ik-screenshot.png)|
