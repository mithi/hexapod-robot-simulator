[![](https://img.shields.io/badge/Buy%20me%20-coffee!-orange.svg?logo=buy-me-a-coffee&color=795548)](https://ko-fi.com/minimithi)
[![Build Status](https://travis-ci.com/mithi/hexapod-robot-simulator.svg?branch=master)](https://travis-ci.com/github/mithi/hexapod-robot-simulator) 
[![codecov](https://codecov.io/gh/mithi/hexapod-robot-simulator/branch/master/graph/badge.svg)](https://codecov.io/gh/mithi/hexapod-robot-simulator)
[![Code Climate](https://codeclimate.com/github/mithi/hexapod-robot-simulator/badges/gpa.svg)](https://codeclimate.com/github/mithi/hexapod-robot-simulator)
[![](https://img.shields.io/codeclimate/tech-debt/mithi/hexapod-robot-simulator)](https://codeclimate.com/github/mithi/hexapod-robot-simulator/trends/technical_debt)
[![HitCount](https://hits.dwyl.com/mithi/hexapod-robot-simulator.svg)](https://hits.dwyl.com/mithi/hexapod-robot-simulator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 
[![PRs welcome!](https://img.shields.io/badge/contributions-welcome-orange.svg?style=flat)](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) 
[![first-timers-only](https://img.shields.io/badge/first--timers--only-friendly-blueviolet.svg?style=flat)](https://www.firsttimersonly.com/)

# Mithi's Hexapod Robot Simulator

- A bare minimum browser-based hexapod robot simulator built from first principles 🕷️
- If you like this project, consider [buying me a few ☕ cups of coffee](https://ko-fi.com/minimithi). 💕

|  |  |  |  |
|---------|---------|---------|---------|
|![Twisting turning and tilting](https://mithi.github.io/robotics-blog/robot-only-x1.gif)|<img src="https://mithi.github.io/robotics-blog/v2-hexapod-1.gif" width="550"/>|<img src="https://mithi.github.io/robotics-blog/v2-hexapod-2.gif" width="500"/>|![Adjusting camera view](https://mithi.github.io/robotics-blog/robot-only-x3.gif)|

# Announcement

You might be interested in checking out my [rewrite in Javascript](http://github.com/mithi/hexapod), live at: https://hexapod.netlify.app/ , which is like 10000000x faster. If you'd like to build you're own user interface with Node, you can download the algorithm alone as a package in the npm registry: [Hexapod Kinematics Library](https://github.com/mithi/hexapod-kinematics-library). There is also [a "fork" modified where you can use the app to control a physical hexapod robot](https://github.com/mithi/hexapod-irl) as you can see in the gif below. 

<p align="center">
    <img src="https://user-images.githubusercontent.com/1670421/103467765-451a2180-4d8d-11eb-8f94-1a23201595b9.gif" alt="drawing" />
</p>

# Features

| STATUS | FEATURE   | DESCRIPTION  |
|---|-----------|--------------|
| 🎉 | Forward Kinematics | Given the angles of each joint, what does the robot look like?|
| 🎉 | Inverse Kinematics | What are the angles of each joint to make the robot look the way I want? Is it even possible? Why or why not? |
| 🎉 | Uniform Movements |  If all of the legs behaved the same way, how will the hexapod robot as a whole behave? |
| 🎉 | Customizability | Set the dimensions and shape of the robot's body and legs. (6 parameters) |
| 🎉 | Usability | Control the camera view, pan, tilt, zoom, whatever. |
| 🎉 | Simplicity | Minimal dependencies. Depends solely on Numpy for calculations. Uses only Plotly Dash for plotting, Dash can be safely replaced if a better 3d plotting library is available. |
| ❗ | Stability Check (WIP) | If we pose the robot in a particular way, will it fall over? |
| ❗ | Fast | Okay, it's not as fast as I wanted, but when run locally, it's okay |
| ❗ | Bug-free | Fine, right now there's still room for improvement |
| ❗ | Well-tested | Yeah, I need to compile test cases first |

## Preview

|![image](https://mithi.github.io/robotics-blog/v2-ik-ui.gif)|![image](https://mithi.github.io/robotics-blog/v2-kinematics-ui.gif)|
|----|----|
| ![image](https://mithi.github.io/robotics-blog/UI-1.gif) | ![image](https://mithi.github.io/robotics-blog/UI-2.gif) |

## Requirements

- [x] Python 3.8.1
- [x] Plotly Dash 1.10.0
- [x] Plotly Dash Daq 0.4.0
- [x] Numpy 1.18.1
- [x] See also [./requirements.txt](./requirements.txt)

## Run

```bash
$ python index.py
Running on http://127.0.0.1:8050/
```

- Modify default settings with [./settings.py](./settings.py)
- Dark Mode is the default - modify page styles with [./style_settings.py](./style_settings.py)

## ⚠️ Known Issues

- [ ] ❗[Good First Issue](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
- [ ] ❗[Help Wanted](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
- [ ] ❗[Bugs](https://github.com/mithi/hexapod-robot-simulator/issues?q=is%3Aissue+is%3Aopen+label%3Abug)
- [ ] ❗[All](https://github.com/mithi/hexapod-robot-simulator/issues)

## Screenshots

| ![Kinematics](https://mithi.github.io/robotics-blog/v2-kinematics-screenshot.png)|
|---|
| ![IK](https://mithi.github.io/robotics-blog/v2-ik-screenshot.png)|

## Conventions and Algorithms

- Definitions
  - [`Linkage`](./hexapod/linkage.py)
  - [`VirtualHexapod`](./hexapod/models.py)
- The [Inverse Kinematics Algorithm](./hexapod/ik_solver/README.md) used for this project
- How to find the orientation of the hexapod with respect to the ground given we know all the orientations of the six legs with respect to the robot's body.
  - [Algorithm 1](./hexapod/ground_contact_solver/ground_contact_solver.py) when we know which of the three points of each leg could contact the ground
  - [Algorithm 2](./hexapod/ground_contact_solver/ground_contact_solver2.py) when  we **don't** know which of points of which legs could be in contact with the ground
- [How to make the hexapod step on the correct target ground contacts](./hexapod/ik_solver/recompute_hexapod.py)
- How to determine if the hexapod should twist and by how much
  - [`find_if_might_twist`](./hexapod/models.py#L248)
  - [`find_twist_frame`](./hexapod/models.py#L273)
  
## Notes

- Now live on https://hexapod-robot-simulator.herokuapp.com ! **BUT** (and a big one) I highly suggest that you run it locally. When run locally, it's pretty speedy! On the other hand, the link above is barely usable. 

- This implementation uses matrices, **NOT** quaternions. I'm aware that quaternions is far superior in every single way. In the (un)forseeable future, maybe?

- Honestly, [my Inverse Kinematics algorithm](./hexapod/ik_solver/README.md) and [orientation algorithm](./hexapod/ground_contact_solver) is just something I came up with based on what I remember back in college plus browsing through the [Mathematics Stack Exchange](https://math.stackexchange.com/). It's just the most intuitive that I can think of. If you want something closer to the state-of-the-art, maybe checkout [Unity's Fast IK](https://assetstore.unity.com/packages/tools/animation/fast-ik-139972) or [ROS IKFast](http://wiki.ros.org/Industrial/Tutorials/Create_a_Fast_IK_Solution).

- Don't be mean! [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](https://www.contributor-covenant.org/)

## 🤗 Contributors

- [@mithi](https://github.com/mithi/)
- [@philippeitis](https://github.com/philippeitis/)
- [@mikong](https://github.com/mikong/)
- [@guilyx](https://github.com/guilyx)
- [@markkulube](https://github.com/markkulube)

![](https://img.shields.io/github/last-commit/mithi/hexapod-robot-simulator)
![](https://img.shields.io/github/commit-activity/y/mithi/hexapod-robot-simulator)
![](https://img.shields.io/github/languages/code-size/mithi/hexapod-robot-simulator?color=yellow)
![](https://img.shields.io/github/repo-size/mithi/hexapod-robot-simulator?color=violet)
![](https://tokei.rs/b1/github/mithi/hexapod-robot-simulator?category=blanks)
![](https://tokei.rs/b1/github/mithi/hexapod-robot-simulator?category=lines)
![](https://tokei.rs/b1/github/mithi/hexapod-robot-simulator?category=files)
![](https://tokei.rs/b1/github/mithi/hexapod-robot-simulator?category=comments)
![](https://tokei.rs/b1/github/mithi/hexapod-robot-simulator?category=code)
![](https://img.shields.io/github/languages/top/mithi/hexapod-robot-simulator)
