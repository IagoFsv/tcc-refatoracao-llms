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


class AnimationSettings:
    def __init__(self, width_rectangle, height_reference):
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference


def draw_array(display, arrTexts, settings):
    texts = tuple(text.value for text in arrTexts)
    display.frames.append((texts, tuple(), settings.width_rectangle, settings.height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(display, arrTexts, settings, *args):
    width_reference, height_reference, arr, i, j = args
    draw_array(display, arrTexts, settings)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, settings, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True


def simulate_heapsort(arr, arrTexts, display, settings):
    def heapify(arr, arrTexts, display, settings, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(
            display, arrTexts, settings, arr, largest, l
        ):
            largest = l
        if r < n and compare_elements(
            display, arrTexts, settings, arr, largest, r
        ):
            largest = r
        if largest != i:
            compare_elements(
                display, arrTexts, settings, arr, i, largest
            )
            swap_elements(arr, arrTexts, i, largest)
            heapify(
                arr, arrTexts, display, settings, n, largest
            )

    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, arrTexts, display, settings, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(arr, arrTexts, display, settings, i, 0)
    draw_array(display, arrTexts, settings)
    clock.tick(FREQUENCY_CLOCK)


def run(values, width_rectangle, height_reference):
    """Sorts a copy of values, animating each step. Public entry point of this unit.

    Returns (sorted list, frames drawn, clock tick rates).
    Each frame is (texts, highlighted positions, width, height).
    """
    arr = list(values)
    texts = [_Text(str(x)) for x in arr]
    screen = _Screen()
    clock.ticks.clear()
    settings = AnimationSettings(width_rectangle, height_reference)
    simulate_heapsort(arr, texts, screen, settings)
    return arr, screen.frames, list(clock.ticks)
