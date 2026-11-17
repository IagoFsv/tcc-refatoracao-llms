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


class AnimationSettings:
    """Keeps the animation settings."""

    def __init__(self, width_rectangle, height_reference):
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference


class HeapSortAnimation:
    """Animation of a sort, frame by frame."""

    def __init__(self, animation_settings, values):
        self.animation_settings = animation_settings
        self.values = values
        self.texts = [_Text(str(x)) for x in self.values]
        self.screen = _Screen()
        self.clock = _Clock()

    def draw_array(self, display, arrTexts, width_rectangle, height_reference):
        display.frames.append((arrTexts, (), width_rectangle, height_reference))

    def swap_elements(self, arr, arrText, i, j):
        arr[i], arr[j] = arr[j], arr[i]
        arrText[i], arrText[j] = arrText[j], arrText[i]

    def compare_elements(self, display, arrTexts, *args):
        width_reference, height_reference, arr, i, j = args
        self.draw_array(display, arrTexts, self.animation_settings.width_rectangle, height_reference)
        self.clock.tick(FREQUENCY_CLOCK)
        self.draw_array(display, arrTexts, self.animation_settings.width_rectangle, height_reference, [i, j])
        self.clock.tick(FREQUENCY_CLOCK)
        if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
            return False
        return True

    def simulate_heapsort(self):
        n = len(self.values)
        def heapify(arr, arrTexts, display, n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            if l < n and self.compare_elements(
                display, arrTexts, self.animation_settings.width_rectangle, self.animation_settings.height_reference, arr, largest, l
            ):
                largest = l
            if r < n and self.compare_elements(
                display, arrTexts, self.animation_settings.width_rectangle, self.animation_settings.height_reference, arr, largest, r
            ):
                largest = r
            if largest != i:
                self.compare_elements(
                    display, arrTexts, self.animation_settings.width_rectangle, self.animation_settings.height_reference, arr, i, largest
                )
                self.swap_elements(arr, arrTexts, i, largest)
                heapify(
                    arr, arrTexts, display, n, largest
                )

        for i in range(n, -1, -1):
            heapify(arr, arrTexts, display, n, i)
        for i in range(n - 1, 0, -1):
            self.swap_elements(arr, arrTexts, i, 0)
            heapify(arr, arrTexts, display, i, 0)
        self.draw_array(display, arrTexts, self.animation_settings.width_rectangle, self.animation_settings.height_reference)
        self.clock.tick(FREQUENCY_CLOCK)

    def run(self):
        """Sorts a copy of values, animating each step. Public entry point of this unit.

        Returns (sorted list, frames drawn, clock tick rates).
        Each frame is (texts, highlighted positions, width, height).
        """
        display = _Screen()
        self.clock.ticks.clear()
        self.simulate_heapsort()
        return self.values, display.frames, list(self.clock.ticks)


def run(values, width_rectangle, height_reference):
    animation_settings = AnimationSettings(width_rectangle, height_reference)
    animation = HeapSortAnimation(animation_settings, values)
    return animation.run()
