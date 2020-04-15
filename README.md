# [☕](https://ko-fi.com/minimithi) [![Code Climate](https://codeclimate.com/github/mithi/hexapod-robot-simulator/badges/gpa.svg)](https://codeclimate.com/github/mithi/hexapod-robot-simulator) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) [![HitCount](https://hits.dwyl.com/mithi/hexapod-robot-simulator.svg)](https://hits.dwyl.com/mithi/hexapod-robot-simulator) [![Build Status](https://travis-ci.com/mithi/hexapod-robot-simulator.svg?branch=master)](https://travis-ci.com/github/mithi/hexapod-robot-simulator)

# 🕷️ Mithi's Hexapod Robot Simulator

- A bare minimum browser-based hexapod robot simulator built from first principles 🕷️
- If you like this project, consider [buying me a few ☕ cups of coffee](https://ko-fi.com/minimithi). 💕

|![Twisting turning and tilting](https://mithi.github.io/robotics-blog/robot-only-x1.gif)|![Leg pattern movements](https://mithi.github.io/robotics-blog/robot-only-x2.gif)|![Customizing Hexapod Dimensions](https://mithi.github.io/robotics-blog/robot-only-x3.gif)|![Adjusting camera view](https://mithi.github.io/robotics-blog/robot-only-x4.gif)|
|---------|---------|---------|---------|
| . | . | . | . |

| STATUS | FEATURE   | DESCRIPTION  |
|---|-----------|--------------|
| 🎉 | Forward Kinematics | Given angles of each joint, what does the robot look like?|
| 🎉 | Inverse Kinematics | What are the angles of each joint to make the robot look the way I want? Is it even possible? Why or why not? |
| 🎉 | Uniform Movements | If all of the legs behaved the same way, what will the robot look like? |
| 🎉 | Customizability | Set the dimensions and shape of the robot's body and legs. (6 parameters) |
| 🎉 | Usability | Control the camera view, pan, tilt, zoom, whatever. |
| 🎉 | Simplicity | Minimal dependencies. Depends solely on Numpy for calculations. Uses only Plotly-dash for plotting, Dash can be safely replaced if a better 3d plotting library is available. |
| ❗ | Stability Check (WIP) | If we pose the robot in a particular way, will it fall over? |
| ❗ | Fast | Okay, it's not as fast as I wanted, but on a local server, it's okay |
| ❗ | Bug-free | Fine, right now there's still room for improvement |
| ❗ | Well-tested | Yeah, I need to compile test cases first |

## 🕷️ Preview

| ![Inverse Kinematics](https://mithi.github.io/robotics-blog/UI-1.gif) | ![Kinematics](https://mithi.github.io/robotics-blog/UI-2.gif) |
|----|----|
| . | . |

## 🕷️ Requirements

- [x] Python 3.8.1
- [x] Plotly Dash 1.10.0
- [x] Plotly Dash Daq 0.4.0
- [x] Numpy 1.18.1
- [x] See also [./requirements.txt](./requirements.txt)

## 🕷️ Run

```bash
$ python index.py
Running on http://127.0.0.1:8050/
```

- Modify default settings in [./settings.py](./settings.py)
- Dark Mode default - modify default style settings in [./style_settings.py](./style_settings.py)

## Conventions and Algorithms

- [Definition of the Leg / Linkage](./hexapod/linkage.py)
- [Inverse Kinematics Algorithm](./hexapod/ik_solver/README.md)
- [Finding ground contact points, tilt and height of hexapod](./hexapod/ground_contact_solver.py)
- [Translate and Rotate Hexapod to correct target ground contacts](./hexapod/ik_solver/recompute_hexapod.py)

## 🕷️ Notes

- ❗Now live on https://hexapod-robot-simulator.herokuapp.com ! **BUT** I highly suggest that you run it on your own local server. When this application is run locally, it's pretty speedy! On the other hand, the link above is barely usable. Might convert this to to be a fully client-side javascript app later, maybe?

- ❗This implementation uses matrices, **NOT** quaternions. I'm aware that quaternions is far superior in every single way. In the (un)forseeable future, maybe?

## ⚠️ Known issues

- [ ] ❗[Priorities](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3APRIORITY)
- [ ] ❗[Help Wanted](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
- [ ] ❗[Bugs](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3Abug)
- [ ] ❗[All](https://github.com/mithi/hexapod-robot-simulator/issues)
