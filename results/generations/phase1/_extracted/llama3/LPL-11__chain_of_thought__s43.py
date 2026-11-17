class Circle:
    def __init__(self, x, y, radius, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


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


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_circle(self, circle):
        """
        Draw a circle on the image.

        @param circle: Circle object
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((circle.y, circle.x), circle.radius, shape=self.image.shape)
        self.image[circle] = circle.color
        return self


def run(size, disk, color=None):
    """size: (rows, columns). disk: Circle object. color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    circle = Circle(*disk)
    if color is None:
        result = image.draw_circle(circle)
    else:
        result = image.draw_circle(circle)
    return result.image
