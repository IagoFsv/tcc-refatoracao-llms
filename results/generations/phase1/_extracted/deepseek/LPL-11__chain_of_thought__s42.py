import skimage
import numpy as np


class Image:
    """
    A class to represent an image.
    """

    def __init__(self, array):
        """
        Create an Image object from a numpy array.

        @param array: numpy array representing the image
        """
        self.image = array


class Circle:
    """
    A class to represent a circle.
    """

    def __init__(self, x, y, radius, color=(0, 0, 0)):
        """
        Create a Circle object.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        @param color: color of the circle
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_circle(self, circle):
        """
        Draw a circle on the image.

        @param circle: Circle object representing the circle to draw
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((circle.y, circle.x), circle.radius, shape=self.image.shape)
        self.image[circle] = circle.color
        return self


def run(size, disk, color=None):
    """size:  (rows, columns). disk: (x, y, radius). color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    x, y, radius = disk
    if color is None:
        result = image.draw_circle(Circle(x, y, radius))
    else:
        result = image.draw_circle(Circle(x, y, radius, color))
    return result.image
