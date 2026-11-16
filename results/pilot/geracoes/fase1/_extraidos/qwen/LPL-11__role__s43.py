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


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_circle(self, circle_params):
        """
        Draw a circle on the image.

        @param circle_params: dictionary containing the parameters for the circle
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((circle_params['y'], circle_params['x']), circle_params['radius'], shape=self.image.shape)
        self.image[circle] = circle_params['color']
        return self


def executar(image_params):
    """image_params: {'tamanho': (linhas, colunas), 'disco': {'x': x, 'y': y, 'raio': raio}, 'cor': (r, g, b)}."""
    imagem = RGB_Image(np.full((*image_params['tamanho'], 3), 255, dtype=np.uint8))
    circle_params = {
        'x': image_params['disco']['x'],
        'y': image_params['disco']['y'],
        'radius': image_params['disco']['raio'],
        'color': image_params.get('cor', (0, 0, 0))
    }
    resultado = imagem.draw_circle(circle_params)
    return resultado.image
