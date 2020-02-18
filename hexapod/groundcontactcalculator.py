
from itertools import combinations
import numpy as np

from .points import Point, cross, vector_from_to, scale, dot, length
from .points import add_vectors, subtract_vectors, get_unit_normal
from .points import is_point_inside_triangle

def set_of_two_trios_from_six():
  # Get all combinations of a three-item-group given six items
  # 20 combinations total
  # (2, 3, 5) is a trio from set [0, 1, 2, 3, 4, 5] 
  # the corresponding other_trio of (2, 3, 5) is (0, 1, 4)
  # order is not important ie (2, 3, 5) is the same as (5, 3, 2)

  trios = [trio for trio in combinations(range(6), 3)]
  other_trios = []

  for trio in trios:
    other_trio = [i for i in filter(lambda x: x not in trio, range(6))]
    other_trios.append(other_trio)

  return trios, other_trios


def get_corresponding_foot_tips(ids, legs):
  i, j, k = ids
  return legs[i].foot_tip(), legs[j].foot_tip(), legs[k].foot_tip()


def check_stability(a, b, c):
  # if the center of gravity p (0, 0) on xy plane
  # is inside projection (in the xy plane) of 
  # the triangle defined by point a, b, c, then this is stable
  p = Point(0, 0, 0)
  return is_point_inside_triangle(p, a, b, c)


def three_ids_of_legs_on_ground(legs):
  trios, other_trios = set_of_two_trios_from_six()

  for trio, other_trio in zip(trios, other_trios):
    # let p0 to p6 be the foot tip of each leg
    p0, p1, p2 = get_corresponding_foot_tips(trio, legs)

    if check_stability(p0, p1, p2) == True:

      # the vector normal to plane defined by these points
      # IMPORTANT: Normal is always pointing up
      # because of how we specified the order of the trio
      # (and the legs in general)
      # starting from middle-right (id:0) to right back (id:5)
      # always towards one direction (ccw)
      n = get_unit_normal(p0, p1, p2)
      
      # p0 is vector from cog (0, 0, 0) to foot tip
      # dot product of this and normal we get the 
      # hypothetical (negative) height of foot_tip to cog
      #
      #  cog *  ^ (normal_vector) ----
      #      \  |                  |
      #       \ |                 height
      #        \|                  |
      #         V p0 (foot_tip) ---V---
      #
      # using p0, p1 or p2 should yield the same result
      h = dot(n, p0)

      # h should be the most negative(the lowest) since
      # the plane defined by this trio is on the ground
      #  the other legs foot tip cannot be lower than the ground
      condition_violated = False
      p3, p4, p5 = get_corresponding_foot_tips(other_trio, legs)
      for p in [p3, p4, p5]:
        h_ = dot(n, p)

        # this combination of legs is wrong, check another
        if h_ < h:
          condition_violated = True
          break
      
      if condition_violated:
        continue
      else:
        # All conditions are met! You've found it!
        return trio

  # nothing met the condition
  return None


def get_legs_on_ground(legs):

  def foot_tip_height(leg):
    return leg.foot_tip_height()
  
  def within_thresh(a, b, tol=2):
    return np.abs(a - b) < 2

  sorted_legs = sorted(legs, key=foot_tip_height, reverse=True)

  # this is negative only foot tip is higher 
  # than center of gravity (0, 0)
  if sorted_legs[0].foot_tip_height() <= 0:
    return None, None

  trio = three_ids_of_legs_on_ground(legs)

  if trio is None:
    return None, None

  p0, p1, p2 = get_corresponding_foot_tips(trio, legs)
  n = get_unit_normal(p0, p1, p2)
  # using p0, p1 or p2 should yield the same result
  cog_from_ground= -dot(n, p0)

  legs_on_ground = []

  for leg in legs:
    tip_from_ground = -dot(n, leg.foot_tip())   
    if within_thresh(tip_from_ground, cog_from_ground):
      legs_on_ground.append(leg)

  return legs_on_ground, None
