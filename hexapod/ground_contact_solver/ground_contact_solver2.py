"""
❗❗❗
This is a more general algorithm to account for the cases that are
not handled correctly by the other ground_contact_solver.
This will only be used by the kinematics-page of the app.
This algorithm can be optimized or replaced if a more elegant
algorithm is available.
❗❗❗

We have 18 points total.
(6 legs, three possible points per leg)

We have a total of 540 combinations
- get three legs out of six (20 combinations)
  - we have three possible points for each leg, that's 27 (3^3)
  -  27 * 20 is 540

For each combination:
    1. Check if stable if not, next
      - Check if the projection of the center of gravity to the plane
        defined by the three points lies inside the triangle, if not, next
    2. Get the height and normal of the height and normal of the triangle plane
        (We need this for the next part)
    3. For each of the three leg, check if the two other points on the leg is not a
        lower height, if condition if broken, next. (6 points total)
    4. For each of the three other legs, check all points (3 points of each leg)
        if so, next. (9 points total)
    5. If no condition is violated, then this is good, return this!
        (height, n_axis, 3 ground contacts)
"""
import hexapod.ground_contact_solver.ground_contact_solver as gc


# ❗Will be replaced
def compute_orientation_properties(legs):
    return gc.compute_orientation_properties(legs)
