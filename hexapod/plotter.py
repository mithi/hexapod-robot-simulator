import plotly.graph_objects as go

class HexapodPlot:
  LINE_SIZE = 10
  HEAD_SIZE = 15
  COG_SIZE = 10
  BODY_COLOR = '#8e44ad'
  COG_COLOR = '#e74c3c'
  LEG_COLOR = '#2c3e50'

  def __init__(self, _hexapod):
    self.hexapod = _hexapod
    self.fig = self._configure()
    self.draw()
    self._configure()

  def _configure(self):
    
    f, m, s = self.hexapod.body_measurements
    a, b, c = self.hexapod.linkage_measurements
    RANGE = (f + m + s + a + b + c)
    AXIS_RANGE = [-RANGE, RANGE]

    fig = go.FigureWidget()
    s = 1.4
    camera = {
    'up': {'x':0, 'y':0, 'z':1},
    'center': {'x':-0.05, 'y':0, 'z':-0.1},
    'eye': {'x':s * 0.25, 'y':s * 0.5, 'z':s * 0.35}
    }
  
    fig['layout'] = {
      'legend': {'x': 0, 'y': 0},
      'scene_camera': camera,
      'margin': {'l': 10, 'b': 20, 't': 20, 'r': 10},
      'scene': {
        'xaxis': {'nticks': 1, 'range': AXIS_RANGE, 'showbackground': False},
        'yaxis': {'nticks': 1, 'range': AXIS_RANGE, 'showbackground': False},
        'zaxis': {'nticks': 1, 'range': AXIS_RANGE, 'backgroundcolor': 'rgb(230, 230, 2005)', 'showbackground': True},
        'aspectmode': 'manual',
        'aspectratio': {'x':1, 'y': 1, 'z': 1}
      }
    }
    return fig

  def _draw_lines(self, _name, _points, _size, _color, _is_name_visible=True):
    self.fig.add_trace(go.Scatter3d(
      name=_name,
      x=[point.x for point in _points],
      y=[point.y for point in _points],
      z=[point.z for point in _points],
      line={
        'color': _color,
        'width': _size
      },
      showlegend=_is_name_visible
    ))

  def _draw_point(self, _name, _point, _size, _color):
    self.fig.add_trace(go.Scatter3d(
      name=_name,
      x=[_point.x],
      y=[_point.y],
      z=[_point.z],
      mode='markers',
      marker={
        'size': _size,
        'color': _color,
        'opacity': 1.0
      }
    ))

  def draw(self):
    # Add body outline
    points = self.hexapod.body.vertices
    self._draw_lines('body', points + [points[0]], HexapodPlot.LINE_SIZE, HexapodPlot.BODY_COLOR)

    # Add head and center of gravity
    self._draw_point('cog', self.hexapod.body.cog, HexapodPlot.COG_SIZE, HexapodPlot.COG_COLOR)
    self._draw_point('head', self.hexapod.body.head, HexapodPlot.HEAD_SIZE, HexapodPlot.BODY_COLOR)

    # Draw legs
    for leg in self.hexapod.legs:
      points = [leg.p0, leg.p1, leg.p2, leg.p3]
      self._draw_lines('leg', points, HexapodPlot.LINE_SIZE, HexapodPlot.LEG_COLOR, False)
    return self.fig
  
  def figure(self):
    return self.fig

  def update(self, hexapod, fig):
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

  def change_camera_view(self, camera, fig):
    fig['layout']['scene_camera'] = camera
    return fig
