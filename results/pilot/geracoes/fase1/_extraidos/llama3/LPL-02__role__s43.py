def executar(lotes):
    """Treina por uma epoca. Ponto de entrada publico desta unidade.

    lotes: lista de (amostras, rotulos); cada amostra tem um score por classe.
    Devolve (perda, acuracia, vies final do modelo, modelo em modo de treino).
    """
    TrainParams = SimpleNamespace(
        modelo=_Modelo(),
        device="cpu",
        train_loader=DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes]),
        optimizer=_Otimizador(modelo),
        criterion=_Perda
    )

    return train(**TrainParams.__dict__)
