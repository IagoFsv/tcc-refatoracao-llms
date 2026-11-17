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


class SortAnimation:
    """Keeps the animation state and behavior."""

    def __init__(self, display, width_reference, height_reference):
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference

    def draw_array(self, arrTexts):
        self.display.frames.append((tuple(text.value for text in arrTexts), (), self.width_reference, self.height_reference))

    def tick(self):
        self.display.frames.append(())
        clock.tick(FREQUENCY_CLOCK)

    def compare_elements(self, arrTexts, i, j):
        self.draw_array(arrTexts)
        self.tick()
        self.draw_array(arrTexts, [i, j])
        self.tick()
        if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
            return False
        return True

    def compare_and_swap(self, arrTexts, i, j):
        self.draw_array(arrTexts)
        self.tick()
        self.draw_array(arrTexts, [i, j])
        self.tick()
        if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
            arr[i], arr[j] = arr[j], arr[i]
            self.draw_array(arrTexts, [i, j])
            self.tick()
        self.draw_array(arrTexts)
        self.tick()
        return True


def run(values):
    """Sorts a copy of values, animating each step. Public entry point of this unit.

    Returns (sorted list, frames drawn, clock tick rates).
    Each frame is (texts, highlighted positions, width, height).
    """
    arr = list(values)
    texts = [_Text(str(x)) for x in arr]
    screen = _Screen()
    clock.ticks.clear()
    animation = SortAnimation(screen, 40, 100)
    animation.draw_array(texts)
    clock.tick(FREQUENCY_CLOCK)
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if not animation.compare_elements(texts, i, j):
                if not animation.compare_and_swap(texts, i, j):
                    break
    animation.draw_array(texts)
    clock.tick(FREQUENCY_CLOCK)
    return arr, screen.frames, list(clock.ticks)
