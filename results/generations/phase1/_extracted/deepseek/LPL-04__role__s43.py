"""Animation of a sort, frame by frame.

Public entry point: run(values). Do not change its name or signature; the
rest of the file may be freely reorganized.

The screen and the clock are minimal versions. The screen keeps every frame
drawn  (texts in the current order, highlighted positions, reference width
and height); the clock keeps the rate requested at each tick.
"""

FREQUENCY_CLOCK = 3


class _Text:
    """Already rendered text of an element."""

    def __init__(self, value):
        self.value = value


class _Screen:
    """Keeps the frames instead of drawing them."""

    def __init__(self):
        self.frames = []


class _Clock:
    """Keeps the rate of each tick instead of waiting."""

    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)


clock = _Clock()


class ParameterObject:
    def __init__(self, display, arrTexts, width_reference, height_reference, arr, i, j):
        self.display = display
        self.arrTexts = arrTexts
        self.width_reference = width_reference
        self.height_reference = height_reference
        self.arr = arr
        self.i = i
        self.j = j


def draw_array(parameter_object):
    texts = tuple(text.value for text in parameter_object.arrTexts)
    parameter_object.display.frames.append((texts, tuple([parameter_object.i, parameter_object.j]),
                                            parameter_object.width_reference, parameter_object.height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(parameter_object):
    draw_array(parameter_object)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(parameter_object)
    clock.tick(FREQUENCY_CLOCK)
    if (parameter_object.arr[parameter_object.i] > parameter_object.arr[parameter_object.j] and parameter_object.i < parameter_object.j) or \
            (parameter_object.arr[parameter_object.i] < parameter_object.arr[parameter_object.j] and parameter_object.i > parameter_object.j):
        return False
    return True


def compare_and_swap(parameter_object):
    swapped = False
    draw_array(parameter_object)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(parameter_object)
    clock.tick(FREQUENCY_CLOCK)
    if (parameter_object.arr[parameter_object.i] > parameter_object.arr[parameter_object.j] and parameter_object.i < parameter_object.j) or \
            (parameter_object.arr[parameter_object.i] < parameter_object.arr[parameter_object.j] and parameter_object.i > parameter_object.j):
        swap_elements(parameter_object.arr, parameter_object.arrTexts, parameter_object.i, parameter_object.j)
        draw_array(parameter_object)
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(parameter_object)
    clock.tick(FREQUENCY_CLOCK)
    return swapped


def simulate_quicksort(arr, arrTexts, display, width_reference, height_reference):
    def partition(parameter_object):
        i = parameter_object.low - 1
        for j in range(parameter_object.low, parameter_object.high):
            if compare_elements(ParameterObject(parameter_object.display, parameter_object.arrTexts,
                                               parameter_object.width_reference, parameter_object.height_reference,
                                               parameter_object.arr, j, parameter_object.high)):
                i += 1
                if i != j:
                    compare_and_swap(ParameterObject(parameter_object.display, parameter_object.arrTexts,
                                                    parameter_object.width_reference, parameter_object.height_reference,
                                                    parameter_object.arr, i, j))
        if i + 1 != parameter_object.high:
            compare_and_swap(ParameterObject(parameter_object.display, parameter_object.arrTexts,
                                            parameter_object.width_reference, parameter_object.height_reference,
                                            parameter_object.arr, i + 1, parameter_object.high))
        return i + 1

    def quicksort(parameter_object):
        if parameter_object.low < parameter_object.high:
            pi = partition(parameter_object)
            quicksort(ParameterObject(parameter_object.display, parameter_object.arrTexts,
                                      parameter_object.width_reference, parameter_object.height_reference,
                                      parameter_object.arr, parameter_object.low, pi - 1))
            quicksort(ParameterObject(parameter_object.display, parameter_object.arrTexts,
                                      parameter_object.width_reference, parameter_object.height_reference,
                                      parameter_object.arr, pi + 1, parameter_object.high))

    quicksort(ParameterObject(display, arrTexts, width_reference, height_reference, arr, 0, len(arr) - 1))
    draw_array(ParameterObject(display, arrTexts, width_reference, height_reference, arr, 0, 0))
    clock.tick(FREQUENCY_CLOCK)


def run(values):
    """Sorts a copy of values, animating each step. Public entry point of this unit.

    Returns  (sorted list, frames drawn, clock tick rates).
    Each frame is  (texts, highlighted positions, width, height).
    """
    arr = list(values)
    texts = [_Text(str(x)) for x in arr]
    screen = _Screen()
    clock.ticks.clear()
    simulate_quicksort(arr, texts, screen, 40, 100)
    return arr, screen.frames, list(clock.ticks)
