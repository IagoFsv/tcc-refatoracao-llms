class AnimationSettings:
    def __init__(self, width_reference, height_reference):
        self.width_reference = width_reference
        self.height_reference = height_reference

class HeapSortAnimation:
    def __init__(self, display, arrTexts, animation_settings):
        self.display = display
        self.arrTexts = arrTexts
        self.animation_settings = animation_settings

    def draw_array(self):
        textos = tuple(texto.valor for texto in self.arrTexts)
        self.display.quadros.append((textos, tuple(), self.animation_settings.width_reference, self.animation_settings.height_reference))

    def swap_elements(self, i, j):
        self.arrTexts[i], self.arrTexts[j] = self.arrTexts[j], self.arrTexts[i]

    def compare_elements(self, i, j):
        self.draw_array()
        clock.tick(FREQUENCY_CLOCK)
        self.draw_array([i, j])
        clock.tick(FREQUENCY_CLOCK)
        if (self.arrTexts[i].valor > self.arrTexts[j].valor and i < j) or (self.arrTexts[i].valor < self.arrTexts[j].valor and i > j):
            return False
        return True

    def heapify(self, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and self.compare_elements(largest, l):
            largest = l
        if r < n and self.compare_elements(largest, r):
            largest = r
        if largest != i:
            self.compare_elements(i, largest)
            self.swap_elements(i, largest)
            self.heapify(n, largest)

    def simulate_heapsort(self):
        n = len(self.arrTexts)
        for i in range(n, -1, -1):
            self.heapify(n, i)
        for i in range(n - 1, 0, -1):
            self.swap_elements(i, 0)
            self.heapify(i, 0)
        self.draw_array()
        clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    animation_settings = AnimationSettings(40, 100)
    heap_sort_animation = HeapSortAnimation(tela, textos, animation_settings)
    heap_sort_animation.simulate_heapsort()
    return arr, tela.quadros, list(clock.ticks)
