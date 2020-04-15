# The Inverse Kinematics Algorithm

## Overview

```python
# Given we know:
# - The point where the hexapod body connect with each hexapod leg (point p0 aka body contact)
# - Where the hexapod leg should connect with the ground (p3 aka target ground point)
#
# We want to solve for:
# - All the 18 angles (alpha, beta, gamma)
# - All the 12 joint points (coxia joint p1) and (femur joint p2)

```

## Rough algorithm in the hexapod frame

In the hexapod frame, the coxia vector is the projected vector (in the plane of the hexapod body) of the vector from the body contact pointing to the target ground point.

```python
# body_to_foot_vector = vector from p0 to p3
# coxia vector = projection of the body_to_foot vector to the hexapod body (hexagon) plane
#
#                            * (p3) Target foot tip
#          *----*----*      /
#         /           \    /
#        /     cog     \  /
#       *       *       */ (p0) body contact
#        \             /
#         \           /
#          *----*----*
#
# hexapod y_axis
# |
# |
# * - -> hexapod x_axis
```

We can find the angle between the coxia vector wrt to the x axis of the hexapod.
Then we can find the angle alpha which is the relative x axis for each attached linkage
as shown in the figure which is the alpha.

```python
# Relative x-axis, for each attached linkage
# Angle each respective relative angle makes wrt to the
# COXIA_AXES = [0, 45, 135, 180, 225, 315] starting from x0 to x5
#
#         x2          x1
#          \         /
#           *---*---*
#          /    |    \
#         /     |     \
#        /      |      \
#  x3 --*------cog------*-- x0
#        \      |      /
#         \     |     /
#          \    |    /
#           *---*---*
#          /         \
#         x4         x5
#
# hexapod y
#  |
#  |
# * - - hexapod x
```

## Rough algorithm in the local leg frame

```python
# |--coxia-----\ ----
# p0 ------- p1 \    \
#                \ femur
#                 \    \
#                  p2 ---
#                 /    /
#                /   tibia
#               /    /
#             p3 -------
#
# Given / Knowns:
# - point p0
# - point p3
# - coxia length
# - femur length
# - tibia length
# - given p0 and p1 lie on the same known axis
#
# Find /Unknowns:
# p1
# p2
# beta - angle between coxia vector (leg x axis) and femur vector
# gamma - angle between tibia vector and perpendicular vector to femur vector
```

## Definitions and Cases

```python
#
#
# **********************
# DEFINITIONS
# **********************
# p0: Body contact point
# p1: coxia point / coxia joint (point between coxia limb and femur limb)
# p2: tibia point / tibia joint (point between femur limb and tibia limb)
# p3: foot tip / ground contact
# coxia vector - vector from p0 to p1
# hexapod.coxia - coxia vector length
# femur vector - vector from p1 to p2
# hexapod.femur - femur vector length
# tibia vector - vector from p2 to p3
# hexapod.tibia - tibia vector length
# body_to_foot vector - vector from p0 to p3
# coxia_to_foot vector - vector from p1 to p3
# d: coxia_to_foot_length
# body_to_foot_length
#
# rho
#  -- angle between coxia vector (leg x axis) and body to foot vector
#  -- angle between point p1, p0, and p3. (p0 at center)
# theta
#  --- angle between femur vector and coxia to foot vector
#  --- angle between point p2, p1, and p3. (p1 at center)
# phi
#  --- angle between coxia vector (leg x axis) and coxia to foot vector
#
# beta
#  --- angle between coxia vector (leg x axis) and femur vector
#  --- positive is counter clockwise
# gamma
#  --- angle between tibia vector and perpendicular vector to femur vector
#  --- positive is counter clockwise
# alpha
#  --- angle between leg coordinate frame and axis defined by line from
#      hexapod's center of gravity to body contact.
#
#
# For CASE 1 and CASE 2:
#   beta = theta - phi
#     beta is positive when phi < theta (case 1)
#     beta is negative when phi > theta (case 2)
# *****************
# Case 1 (beta IS POSITIVE)
# *****************
#
#      ^          (p2)
#      |            *
#  (leg_z_axis)    / |
#      |          /  |
#      |         /   |
#   (p0)    (p1)/    |
#     *------- *-----| ----------------> (leg_x_axis)
#      \       \     |
#        \      \    |
#          \     \   |
#            \    \  |
#              \   \ |
#                \   |
#                  \ * (p3)
#
#
# *****************
# Case 2 (beta is negative)
# *****************
#                           ^
#                           |
#                         (leg_z_axis direction)
# (p0)     (p1)             |
# *------- *----------------|------> (leg_x_axis direction)
# \        |   \
#  \       |    \
#   \      |     \
#    \     |      * (p2)
#     \    |     /
#      \   |    /
#       \  |   /
#        \ |  /
#         \| /
#          *
#
# *****************
# Case 3 (p3 is above p1) then beta = phi + theta
# *****************
#                * (p2)
#               / \
#             /    |
#           /      * (p3)
#         /     /
# *------ *  /
# (p0)   (p1)
#
#
```
