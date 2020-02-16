from .figure_template import HEXAPOD_FIGURE

class HexapodPlot:
  LINE_SIZE = 10
  HEAD_SIZE = 15
  COG_SIZE = 10
  BODY_COLOR = '#8e44ad'
  COG_COLOR = '#e74c3c'
  LEG_COLOR = '#2c3e50'

  def __init__(self):
    self.fig = HEXAPOD_FIGURE
  
  def update(self, fig, hexapod):
    #body
    points = hexapod.body.vertices + [hexapod.body.vertices[0]]
    fig['data'][0]['x'] = [point.x for point in points]
    fig['data'][0]['y'] = [point.y for point in points]
    fig['data'][0]['z'] = [point.z for point in points]

    fig['data'][2]['x'] = [hexapod.body.head.x]
    fig['data'][2]['y'] = [hexapod.body.head.y]
    fig['data'][2]['z'] = [hexapod.body.head.z]
    
    # legs
    n = [i for i in range(3, 9)]
    
    for n, leg in zip(n, hexapod.legs):
      points = [leg.p0, leg.p1, leg.p2, leg.p3]
      fig['data'][n]['x'] = [point.x for point in points]
      fig['data'][n]['y'] = [point.y for point in points]
      fig['data'][n]['z'] = [point.z for point in points]    

    # Change range of view for all axes
    f, m, s = hexapod.body_measurements
    a, b, c = hexapod.linkage_measurements
    RANGE = (f + m + s + a + b + c)
    AXIS_RANGE = [-RANGE, RANGE]

    fig['layout']['scene']['xaxis']['range'] = AXIS_RANGE
    fig['layout']['scene']['yaxis']['range'] = AXIS_RANGE
    fig['layout']['scene']['zaxis']['range'] = AXIS_RANGE

    return fig

  def change_camera_view(self, fig, camera):
    fig['layout']['scene']['camera'] = camera
    return fig
