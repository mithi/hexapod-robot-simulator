
# Inverse Kinematics Edge Cases

- Coxia point shoved on ground
- Body contact shoved on ground
- Can't reach target ground point
  - Femur length is too long
  - Tibia length is too long
  - The ground is blocking the path
- Legs too short
  - Too many legs off the floor
  - All left legs off the ground
  - All right legs off the ground
- Angle required is beyond range of motion
  - Alpha
  - Beta
  - Gamma

# `VirtualHexapod.Update` Edge Cases

- Unstable. Center of gravity is outside the hexapod's support polygon