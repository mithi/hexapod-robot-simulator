# hexapod-robot-simulator
- Hexapod robot simulator built from first principles

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

## Priorities
  - [ ] Checking pose stability. The inverse kinematics solver doesn't yet actually check if the center of gravity is inside its support polygon.
  - [ ] Sample gifs and video previewing the functionalities of this app
  - [ ] Compiling integration and unit tests cases
  - [ ] A reimplementation of the inverse kinematics solver **`hexapod.ik_solver2`**. The current implementation [`hexapod.ik_solver`](https://github.com/mithi/hexapod-robot-simulator/blob/master/hexapod/ik_solver.py) involves a bunch of tiny helper methods and one big god function that tries to do almost everything. I plan to redesign this by making a class that centers around this responsibility.
  - [ ] Improving the code quality of `hexapod.models` and `hexapod.hexapod.linkage` and  `.hexapod.ground_contact_solver` modules

## Known Issues
  - [ ] ❗ Some unstable poses are not marked as unstable by the hexapod which might be a bug somewhere in [`hexapod.ground_contact_solver.three_ids_of_ground_contacts`](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/ground_contact_solver.py#L45) or [`hexapod.models.VirtualHexapod.update`](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/models.py#L141)
  - [ ] ❗ When the right-middle leg is twisted by itself, the figure point-of-view changes, other legs don't do this. Might be a bug in [`hexapod.models.VirtualHexapod._find_if_might_twist`](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/models.py#L192) or [`hexapod.models.find_twist_frame`](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/models.py#L231)
  - [ ] ❗ Leg can criss-cross each other which shouldn't be the case, I'm open to hearing ideas on how to go about this
  - [ ] [Other issues](https://github.com/mithi/hexapod-robot-simulator/issues)

## Modifying default settings
- See [./CUSTOMIZE.md](./CUSTOMIZE.md) for more information

## Screenshots
| ![](./img/screen_shot-v1-4.png) | ![](./img/screen_shot-v1-2.png) |
| ------------- |:-------------:|
| ![](./img/screen_shot-v1-3.png) | ![](./img/screen_shot-v1-1.png) |
