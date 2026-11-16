# Teste original
config = {"input_size": 10, "n_actions": 5, "hidden_size": 20, "gamma": 0.9, "batch_size": 32,
          "epsilon": 0.1, "epsilon_min": 0.01, "epsilon_decay": 0.9}
result = executar(config)
print(result)  # mesmo resultado que antes

# Teste refatorado
config_obj = Config(10, 5, 20, 0.9, 32, 0.1, 0.01, 0.9)
result = executar(config_obj)
print(result)  # mesmo resultado que antes
