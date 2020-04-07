# hexapod-robot-simulator
- A simple browser-based hexapod robot simulator built from first principles
- You can currently check it out on https://hexapod-robot-simulator.herokuapp.com but I highly suggest that
you run it on your own local server. When this application is run locally it's really snappy! On the other hand, the link above is barely usable.

## Features
#### Forward Kinematics
- Given angles of each joint, what does the robot look like?
#### Inverse Kinematics
- What are the angles of each joint to make the robot look the way I want?
- Is it even possible? Why or why not?
#### Uniform Movements
- If all of the legs behaved the same way, what will the robot look like?
#### Stability Checking (❗❗WIP)
- If we pose the robot in a particular way, will it fall over?
### Customizability
- Set the dimensions and shape of the robot's body and legs. (6 parameters)
#### Usability
- Control the camera view, pan, tilt or zoom.
#### Simplicity
- Only depends on Numpy for calculations
- NOTE: This implementation uses matrices, not quaternions

## Requirements
- Python 3.8.1
- Plotly Dash 1.10.0
- Plotly Dash Daq 0.4.0
- Numpy 1.18.1
- See also [./requirements.txt](./requirements.txt)

## Run
```
$ python index.py
```
- Modify default settings in [./settings.py](./settings.py)

## Priorities
  - [ ] Checking pose stability. The inverse kinematics solver doesn't yet actually check if the center of gravity is inside its support polygon.
  - [ ] Sample gifs and video previewing the functionalities of this app
  - [ ] Compiling integration and unit tests cases
  - [ ] A reimplementation of the inverse kinematics solver **`hexapod.ik_solver2`**. The current implementation [`hexapod.ik_solver`](https://github.com/mithi/hexapod-robot-simulator/blob/master/hexapod/ik_solver.py) involves a bunch of tiny helper methods and one big god function that tries to do almost everything. I plan to redesign this by making a class that centers around this responsibility.
  - [ ] Improving the code quality of `hexapod.models` and `hexapod.hexapod.linkage` and  `.hexapod.ground_contact_solver` modules

## Known Issues
  - [ ] ❗ Some unstable poses are not marked as unstable by the hexapod which might be a bug somewhere in [`hexapod.ground_contact_solver.three_ids_of_ground_contacts`](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/ground_contact_solver.py#L45) or [`hexapod.models.VirtualHexapod.update`](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/models.py#L141)
  - [ ] ❗ When the right-middle leg is twisted by itself (coxia angle changed), the figure point-of-view changes, other legs don't do this. Might be a bug in [`hexapod.models.VirtualHexapod._find_if_might_twist`](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/models.py#L192) or [`hexapod.models.find_twist_frame`](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/models.py#L231)
  - [ ] ❗ Leg can criss-cross each other which shouldn't be the case, I'm open to hearing ideas on how to go about this
  - [ ] [Other issues](https://github.com/mithi/hexapod-robot-simulator/issues)
