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


clock = _Clock()


class SortAnimationParams:
    def __init__(self, arrTexts, width_rectangle, height_reference, poses_elevated=()):
        self.arrTexts = arrTexts
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference
        self.poses_elevated = poses_elevated


class HeapSortParams:
    def __init__(self, arr, arrTexts, display, width_reference, height_reference):
        self.arr = arr
        self.arrTexts = arrTexts
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference


def draw_array(display, params):
    texts = tuple(text.value for text in params.arrTexts)
    display.frames.append((texts, tuple(params.poses_elevated), params.width_rectangle, params.height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(display, params, i, j):
    draw_array(display, params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, params, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[i] > params.arr[j] and i < j) or (params.arr[i] < params.arr[j] and i > j):
        return False
    return True


def heapify(params, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and compare_elements(
        params.display, params, largest, l
    ):
        largest = l
    if r < n and compare_elements(
        params.display, params, largest, r
    ):
        largest = r
    if largest != i:
        compare_elements(
            params.display, params, i, largest
        )
        swap_elements(params.arr, params.arrTexts, i, largest)
        heapify(
            params, n, largest
        )


def simulate_heapsort(params):
    n = len(params.arr)
    for i in range(n, -1, -1):
        heapify(params, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(params.arr, params.arrTexts, i, 0)
        heapify(params, i, 0)
    draw_array(params.display, params)
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
    simulate_heapsort(HeapSortParams(arr, texts, screen, 40, 100))
    return arr, screen.frames, list(clock.ticks)
