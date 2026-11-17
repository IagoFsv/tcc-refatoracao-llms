from dataclasses import dataclass, asdict

FREQUENCY_CLOCK = 3

class _Text:
    def __init__(self, value):
        self.value = value

class _Screen:
    def __init__(self):
        self.frames = []

class _Clock:
    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)

clock = _Clock()

@dataclass
class Display:
    width_rectangle: int
    height_reference: int
    screen: _Screen

@dataclass
class CompareParams:
    display: Display
    arrTexts: list
    arr: list
    width_reference: int
    height_reference: int
    i: int
    j: int

def draw_array(display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
    texts = tuple(text.value for text in arrTexts)
    display.screen.frames.append((texts, tuple(poses_elevated), width_rectangle, height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(compare_params: CompareParams):
    draw_array(
        compare_params.display, 
        compare_params.arrTexts, 
        compare_params.width_reference, 
        compare_params.height_reference
    )
    clock.tick(FREQUENCY_CLOCK)
    draw_array(
        compare_params.display, 
        compare_params.arrTexts, 
        compare_params.width_reference, 
        compare_params.height_reference, 
        [compare_params.i, compare_params.j]
    )
    clock.tick(FREQUENCY_CLOCK)
    if (compare_params.arr[compare_params.i] > compare_params.arr[compare_params.j] and compare_params.i < compare_params.j) or (compare_params.arr[compare_params.i] < compare_params.arr[compare_params.j] and compare_params.i > compare_params.j):
        return False
    return True

def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    def heapify(compare_params):
        n = len(compare_params.arr)
        largest = compare_params.i
        l = 2 * compare_params.i + 1
        r = 2 * compare_params.i + 2
        if l < n and compare_elements(compare_params):
            compare_params.i = l
            heapify(compare_params)
        if r < n and compare_elements(compare_params):
            compare_params.i = r
            heapify(compare_params)
        if compare_params.i != compare_params.largest:
            swap_elements(compare_params.arr, compare_params.arrTexts, compare_params.i, compare_params.largest)
            heapify(compare_params)

    n = len(arr)
    for i in range(n, -1, -1):
        heapify(CompareParams(
            display=display,
            arrTexts=arrTexts,
            arr=arr,
            width_reference=width_reference,
            height_reference=height_reference,
            i=i,
            j=0
        ))
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(CompareParams(
            display=display,
            arrTexts=arrTexts,
            arr=arr[:i],
            width_reference=width_reference,
            height_reference=height_reference,
            i=0,
            j=0
        ))
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)

def run(values):
    arr = list(values)
    texts = [_Text(str(x)) for x in arr]
    screen = _Screen()
    clock.ticks.clear()
    display = Display(width_rectangle=40, height_reference=100, screen=screen)
    simulate_heapsort(arr, texts, display, 40, 100)
    return arr, screen.frames, list(clock.ticks)
