from dataclasses import dataclass, asdict

FREQUENCY_CLOCK = 3


class Text:
    def __init__(self, value):
        self.value = value


class Screen:
    def __init__(self):
        self.frames = []


class Clock:
    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)


clock = Clock()


@dataclass
class Display:
    width_rectangle: int
    height_reference: int
    screen: Screen


@dataclass
class ArrTexts:
    texts: tuple
    poses_elevated: tuple


@dataclass
class Arr:
    arr: list
    arrTexts: ArrTexts
    display: Display


def draw_array(display: Display, arrTexts: ArrTexts, width_rectangle, height_reference, poses_elevated=()):
    texts = tuple(text.value for text in arrTexts.texts)
    display.screen.frames.append((texts, tuple(poses_elevated), width_rectangle, height_reference))


def swap_elements(arr: Arr, i, j):
    arr.arr[i], arr.arr[j] = arr.arr[j], arr.arr[i]
    arr.arrTexts.texts[i], arr.arrTexts.texts[j] = arr.arrTexts.texts[j], arr.arrTexts.texts[i]


def compare_elements(arr: Arr, width_reference, height_reference, i, j):
    draw_array(arr.display, arr.arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(arr.display, arr.arrTexts, width_reference, height_reference, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (arr.arr[i] > arr.arr[j] and i < j) or (arr.arr[i] < arr.arr[j] and i > j):
        return False
    return True


def simulate_heapsort(arr: Arr, display: Display, width_reference, height_reference):
    def heapify(arr: Arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(arr, width_reference, height_reference, arr.arr, largest, l):
            largest = l
        if r < n and compare_elements(arr, width_reference, height_reference, arr.arr, largest, r):
            largest = r
        if largest != i:
            compare_elements(arr, width_reference, height_reference, arr.arr, i, largest)
            swap_elements(arr, i, largest)
            heapify(arr, n, largest)

    n = len(arr.arr)
    for i in range(n, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, i, 0)
        heapify(arr, i, 0)
    draw_array(arr.display, arr.arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)


def run(values):
    arr = Arr(list(values), ArrTexts(tuple([Text(str(x)) for x in values]), ()), Display(40, 100, Screen()))
    clock.ticks.clear()
    simulate_heapsort(arr, arr.display, 40, 100)
    return arr.arr, arr.display.screen.frames, list(clock.ticks)
