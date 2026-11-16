def executar(dimensoes):
    config = DQNConfig(**dimensoes)
    rede = DQN(config)
    return _resumo(rede)
