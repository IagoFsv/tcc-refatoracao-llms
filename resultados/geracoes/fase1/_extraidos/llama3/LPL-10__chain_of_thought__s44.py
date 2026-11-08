# Testes
params1 = DrawingParams((10, 10), (0, 0, 0, 0))
print(executar(params1).shape)  # (10, 10, 3)

params2 = DrawingParams((10, 10), (0, 0, 0, 0), cor=(255, 0, 0))
print(executar(params2).shape)  # (10, 10, 3)
