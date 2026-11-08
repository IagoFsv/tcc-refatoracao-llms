# Testes
ponto = Point(0.5, 0.5)
cantos = Corner(0, 1, 0, 1)
valores = Values(0, 1, 1, 0)
assert executar(ponto, cantos, valores) == 0.5

ponto = Point(0.5, 0.5)
cantos = Corner(0, 1, 0, 1)
valores = Values(0, 1, 1, 0)
assert bilinear_interpolation(ponto, cantos, valores) == 0.5
