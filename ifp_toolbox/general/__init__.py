import numpy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class RectangleSelector(object):
    """
    This is a class that allows the user to interactively select a
    rectangular region in an image and returns the coordinates of the
    upper-left corner and the bottom-right corner.

    Code snippet taken from:
    http://stackoverflow.com/questions/12052379/
    matplotlib-draw-a-selection-area-in-the-shape-of-a-rectangle-with-the-mouse
    """

    def __init__(self):
        self.ax = plt.gca()
        self.rect = Rectangle((0, 0), 1, 1)
        self.customize_rectangle()
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event',
                                          self.on_release)

    def customize_rectangle(self):
        self.rect.set_fill(False)
        self.rect.set_edgecolor('blue')
        self.rect.set_linewidth(3.0)

    def on_press(self, event):
        print 'press'
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_release(self, event):
        print 'release'
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()

    def get_coords(self):
        return [numpy.floor(self.x0),
                numpy.floor(self.y0),
                numpy.ceil(self.x1),
                numpy.ceil(self.y1)]
