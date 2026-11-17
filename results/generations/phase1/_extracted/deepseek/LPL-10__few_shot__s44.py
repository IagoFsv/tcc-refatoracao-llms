from dataclasses import dataclass, asdict

@dataclass
class Segment:
    y0: int
    x0: int
    y1: int
    x1: int

@dataclass
class Color:
    r: int
    g: int
    b: int

class Image:
    def __init__(self, array):
        self.image = array


class RGB_Image(Image):
    def draw_line(self, segment: Segment, color: Color):
        line = skimage.draw.line(segment.y0, segment.x0, segment.y1, segment.x1)
        self.image[line] = asdict(color)
        return self


def run(size, segment, color=None):
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segment
    if color is None:
        result = image.draw_line(Segment(y0, x0, y1, x1), Color(0, 0, 0))
    else:
        r, g, b = color
        result = image.draw_line(Segment(y0, x0, y1, x1), Color(r, g, b))
    return result.image
