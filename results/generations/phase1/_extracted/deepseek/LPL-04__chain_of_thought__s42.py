class Params:
    def __init__(self, width_reference, height_reference, arr, i, j):
        self.width_reference = width_reference
        self.height_reference = height_reference
        self.arr = arr
        self.i = i
        self.j = j


def compare_elements(display, arrTexts, params: Params):
    draw_array(display, arrTexts, params.width_reference, params.height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, params.width_reference, params.height_reference, [params.i, params.j])
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[params.i] > params.arr[params.j] and params.i < params.j) or (params.arr[params.i] < params.arr[params.j] and params.i > params.j):
        return False
    return True


def compare_and_swap(display, arrTexts, params: Params):
    swapped = False
    draw_array(display, arrTexts, params.width_reference, params.height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, params.width_reference, params.height_reference, [params.i, params.j])
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[params.i] > params.arr[params.j] and params.i < params.j) or (params.arr[params.i] < params.arr[params.j] and params.i > params.j):
        swap_elements(params.arr, arrTexts, params.i, params.j)
        draw_array(display, arrTexts, params.width_reference, params.height_reference, [params.i, params.j])
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(display, arrTexts, params.width_reference, params.height_reference)
    clock.tick(FREQUENCY_CLOCK)
    return swapped
