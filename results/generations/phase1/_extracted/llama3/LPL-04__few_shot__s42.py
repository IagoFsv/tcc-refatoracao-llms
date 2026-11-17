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


class SortAnimation:
    """Animation of a sort, frame by frame."""

    def __init__(self, display, width_reference, height_reference):
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference

    def draw_array(self, arrTexts):
        texts = tuple(text.value for text in arrTexts)
        self.display.frames.append((texts, tuple(), self.width_reference, self.height_reference))

    def swap_elements(self, arr, arrTexts, i, j):
        arr[i], arr[j] = arr[j], arr[i]
        arrTexts[i], arrTexts[j] = arrTexts[j], arrTexts[i]

    def compare_elements(self, arrTexts, *args):
        width_reference, height_reference, arr, i, j = args
        self.draw_array(arrTexts)
        self.display.clock.tick(FREQUENCY_CLOCK)
        self.draw_array(arrTexts)
        self.display.clock.tick(FREQUENCY_CLOCK)
        if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
            return False
        return True

    def compare_and_swap(self, arrTexts, *args):
        width_reference, height_reference, arr, i, j = args
        swapped = False
        self.draw_array(arrTexts)
        self.display.clock.tick(FREQUENCY_CLOCK)
        self.draw_array(arrTexts)
        self.display.clock.tick(FREQUENCY_CLOCK)
        if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
            self.swap_elements(arr, arrTexts, i, j)
            self.draw_array(arrTexts)
            self.display.clock.tick(FREQUENCY_CLOCK)
            swapped = True
        self.draw_array(arrTexts)
        self.display.clock.tick(FREQUENCY_CLOCK)
        return swapped

    def simulate_quicksort(self, arr, arrTexts):
        def partition(arr, arrTexts, low, high):
            i = low - 1
            for j in range(low, high):
                if self.compare_elements(arrTexts, self.width_reference, self.height_reference, arr, j, high):
                    i += 1
                    if i != j:
                        self.compare_and_swap(arrTexts, self.width_reference, self.height_reference, arr, i, j)
            if i + 1 != high:
                self.compare_and_swap(arrTexts, self.width_reference, self.height_reference, arr, i + 1, high)
            return i + 1

        def quicksort(arr, arrTexts, low, high):
            if low < high:
                pi = partition(arr, arrTexts, low, high)
                quicksort(arr, arrTexts, low, pi - 1)
                quicksort(arr, arrTexts, pi + 1, high)

        quicksort(arr, arrTexts, 0, len(arr) - 1)
        self.draw_array(arrTexts)
        self.display.clock.tick(FREQUENCY_CLOCK)

    def run(self, values):
        """Sorts a copy of values, animating each step. Public entry point of this unit.

        Returns (sorted list, frames drawn, clock tick rates).
        Each frame is (texts, highlighted positions, width, height).
        """
        arr = list(values)
        texts = [_Text(str(x)) for x in arr]
        self.simulate_quicksort(arr, texts)
        return arr, self.display.frames, self.display.clock.ticks


def main():
    display = _Screen()
    clock = _Clock()
    animation = SortAnimation(display, 40, 100)
    values = [5, 3, 8, 4, 2, 6, 7, 1, 9]
    result = animation.run(values)
    print(result)


if __name__ == "__main__":
    main()
