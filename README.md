# hexapod-robot-simulator
- Hexapod robot simulator built from first principles

# Requirements
- Python 3.8.1
- Plotly Dash 1.10.0
- Numpy 1.18.1

# Run
```
$ python index.py
```

# KNOWN ISSUES
  - [ ]**Priority** The inverse kinematics solver doesn't yet actually check if the current computed pose is stable (IE if the triangle formed by one of combinations of three legs that contact the ground contain the projection of the hexapod's center of gravity).
  - [ ]Some unstable poses are not marked as unstable by the hexapod which might be a bug somewhere in [hexapod.ground_contact_solver. ](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/ground_contact_solver.py#L45) or [hexapod.models.VirtualHexapod.update](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/models.py#L141)
  - [ ]When the right-middle leg is twisted by itself, the figure point-of-view changes, other legs don't do this. Might be a bug in [hexapod.models.VirtualHexapod._find_if_might_twist](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/models.py#L192) or [hexapod.models.find_twist_frame](https://github.com/mithi/hexapod-robot-simulator/blob/e19f5de5b1110bc78bd75091eb63f47907ffddc5/hexapod/models.py#L231)

  - [ ]Leg can criss-cross each other which shouldn't be the case, I'm open to hearing ideas on how to go about this
  - [ ]See other issues [here](https://github.com/mithi/hexapod-robot-simulator/issues)

# Changing global variables
- See [./CUSTOMIZE.md](./CUSTOMIZE.md) for more information

# Screenshots
| ![](./img/screen_shot-v1-4.png) | ![](./img/screen_shot-v1-2.png) |
| ------------- |:-------------:|
| ![](./img/screen_shot-v1-3.png) | ![](./img/screen_shot-v1-1.png) |
