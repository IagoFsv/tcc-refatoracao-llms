class Parameters:
    def __init__(self, width_reference, height_reference, arr, i, j):
        self.width_reference = width_reference
        self.height_reference = height_reference
        self.arr = arr
        self.i = i
        self.j = j

def compare_elements(display, arrTexts, parameters):
    draw_array(display, arrTexts, parameters.width_reference, parameters.height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, parameters.width_reference, parameters.height_reference, [parameters.i, parameters.j])
    clock.tick(FREQUENCY_CLOCK)
    if (parameters.arr[parameters.i] > parameters.arr[parameters.j] and parameters.i < parameters.j) or (parameters.arr[parameters.i] < parameters.arr[parameters.j] and parameters.i > parameters.j):
        return False
    return True

def compare_and_swap(display, arrTexts, parameters):
    swapped = False
    draw_array(display, arrTexts, parameters.width_reference, parameters.height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, parameters.width_reference, parameters.height_reference, [parameters.i, parameters.j])
    clock.tick(FREQUENCY_CLOCK)
    if (parameters.arr[parameters.i] > parameters.arr[parameters.j] and parameters.i < parameters.j) or (parameters.arr[parameters.i] < parameters.arr[parameters.j] and parameters.i > parameters.j):
        swap_elements(parameters.arr, arrTexts, parameters.i, parameters.j)
        draw_array(display, arrTexts, parameters.width_reference, parameters.height_reference, [parameters.i, parameters.j])
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(display, arrTexts, parameters.width_reference, parameters.height_reference)
    clock.tick(FREQUENCY_CLOCK)
    return swapped
