"""Animation of a sort, frame by frame.

Public entry point: run(values). Do not change its name or signature; the
rest of the file may be freely reorganized.

The screen and the clock are minimal versions. The screen keeps every frame
drawn (texts in the current order, highlighted positions, reference width
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


class SortParameters:
    def __init__(self, display, arrTexts, width_reference, height_reference):
        self.display = display
        self.arrTexts = arrTexts
        self.width_reference = width_reference
        self.height_reference = height_reference


clock = _Clock()


def draw_array(params, poses_elevated=()):
    texts = tuple(text.value for text in params.arrTexts)
    params.display.frames.append((texts, tuple(poses_elevated), params.width_reference, params.height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(params, *args):
    i, j = args
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(params, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[i] > params.arr[j] and i < j) or (params.arr[i] < params.arr[j] and i > j):
        return False
    return True


def compare_and_swap(params, *args):
    i, j = args
    swapped = False
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(params, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[i] > params.arr[j] and i < j) or (params.arr[i] < params.arr[j] and i > j):
        swap_elements(params.arr, params.arrTexts, i, j)
        draw_array(params, [i, j])
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    return swapped


def partition(params, low, high):
    i = low - 1
    for j in range(low, high):
        if compare_elements(params, j, high):
            i += 1
            if i != j:
                compare_and_swap(params, i, j)
    if i + 1 != high:
        compare_and_swap(params, i + 1, high)
    return i + 1


def quicksort(params, low, high):
    if low < high:
        pi = partition(params, low, high)
        quicksort(params, low, pi - 1)
        quicksort(params, pi + 1, high)


def simulate_quicksort(arr, arrTexts, display, width_reference, height_reference):
    params = SortParameters(display, arrTexts, width_reference, height_reference)
    params.arr = arr
    quicksort(params, 0, len(arr) - 1)
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)


def run(values):
    """Sorts a copy of values, animating each step. Public entry point of this unit.

    Returns (sorted list, frames drawn, clock tick rates).
    Each frame is (texts, highlighted positions, width, height).
    """
    arr = list(values)
    texts = [_Text(str(x)) for x in arr]
    screen = _Screen()
    clock.ticks.clear()
    simulate_quicksort(arr, texts, screen, 40, 100)
    return arr, screen.frames, list(clock.ticks)
