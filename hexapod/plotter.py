from .templates.figure_template import HEXAPOD_FIGURE

class HexapodPlot:
  def __init__(self):
    self.fig = HEXAPOD_FIGURE

  def _draw_hexapod(self, fig, hexapod):
    #body
    points = hexapod.body.vertices + [hexapod.body.vertices[0]]

    # body surface Mesh
    fig['data'][0]['x'] = [point.x for point in points]
    fig['data'][0]['y'] = [point.y for point in points]
    fig['data'][0]['z'] = [point.z for point in points]

    # body outline
    fig['data'][1]['x'] = fig['data'][0]['x']
    fig['data'][1]['y'] = fig['data'][0]['y']
    fig['data'][1]['z'] = fig['data'][0]['z']

    fig['data'][2]['x'] = [hexapod.body.cog.x]
    fig['data'][2]['y'] = [hexapod.body.cog.y]
    fig['data'][2]['z'] = [hexapod.body.cog.z]

    fig['data'][3]['x'] = [hexapod.body.head.x]
    fig['data'][3]['y'] = [hexapod.body.head.y]
    fig['data'][3]['z'] = [hexapod.body.head.z]

    # legs
    n = [i for i in range(4, 10)]

    for n, leg in zip(n, hexapod.legs):
      points = [leg.p0, leg.p1, leg.p2, leg.p3]
      fig['data'][n]['x'] = [point.x for point in points]
      fig['data'][n]['y'] = [point.y for point in points]
      fig['data'][n]['z'] = [point.z for point in points]

    # draw a mesh for body contact on ground
    ground_contacts = hexapod.ground_contact_points()
    fig['data'][10]['x'] = [point.x for point in ground_contacts]
    fig['data'][10]['y'] = [point.y for point in ground_contacts]
    fig['data'][10]['z'] = [point.z for point in ground_contacts]

    return fig

  def _draw_scene(self, fig, hexapod):
      # Change range of view for all axes
    f, m, s = hexapod.body_measurements
    a, b, c = hexapod.linkage_measurements
    RANGE = (f + m + s + a + b + c)
    AXIS_RANGE = [-RANGE, RANGE]

    z_start = -10
    fig['layout']['scene']['xaxis']['range'] = AXIS_RANGE
    fig['layout']['scene']['yaxis']['range'] = AXIS_RANGE
    fig['layout']['scene']['zaxis']['range'] = [z_start, (RANGE - z_start) * 2]

    axis_scale = f / 2

    # Draw the hexapod local frame
    cog = hexapod.body.cog
    x_axis = hexapod.x_axis
    y_axis = hexapod.y_axis
    z_axis = hexapod.z_axis

    fig['data'][11]['x'] = [cog.x, cog.x + axis_scale * x_axis.x]
    fig['data'][11]['y'] = [cog.y, cog.y + axis_scale * x_axis.y]
    fig['data'][11]['z'] = [cog.z, cog.z + axis_scale * x_axis.z]

    fig['data'][12]['x'] = [cog.x, cog.x + axis_scale * y_axis.x]
    fig['data'][12]['y'] = [cog.y, cog.y + axis_scale * y_axis.y]
    fig['data'][12]['z'] = [cog.z, cog.z + axis_scale * y_axis.z]

    fig['data'][13]['x'] = [cog.x, cog.x + axis_scale * z_axis.x]
    fig['data'][13]['y'] = [cog.y, cog.y + axis_scale * z_axis.y]
    fig['data'][13]['z'] = [cog.z, cog.z + axis_scale * z_axis.z]

    # Scale the global coordinate frame

    fig['data'][14]['x'] = [0, axis_scale]
    fig['data'][14]['y'] = [0, 0]
    fig['data'][14]['z'] = [0, 0]

    fig['data'][15]['x'] = [0, 0]
    fig['data'][15]['y'] = [0, axis_scale]
    fig['data'][15]['z'] = [0, 0]

    fig['data'][16]['x'] = [0, 0]
    fig['data'][16]['y'] = [0, 0]
    fig['data'][16]['z'] = [0, axis_scale]

    return fig

  def update(self, fig, hexapod):
    fig = self._draw_hexapod(fig, hexapod)
    fig = self._draw_scene(fig, hexapod)
    return fig

  def change_camera_view(self, fig, camera):
    fig['layout']['scene']['camera'] = camera
    return fig
