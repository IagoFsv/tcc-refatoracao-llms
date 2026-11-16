class ParameterObject:
    """Object to hold all parameters for refactoring purposes."""

    def __init__(self, device, train_loader, optimizer, criterion):
        self.device = device
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion


def train(
        model:nn.modules,
        parameters: ParameterObject
         )->tuple[float, float, nn.Module]:
    '''
    basic train function generate by github-copilot
    args
        model: model to train
        parameters: ParameterObject containing all parameters for training
    return
        train_loss: loss of the training process
        accuracy: accuracy of the training process
        model: trained model
    '''
    model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(parameters.train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(parameters.device), target.to(parameters.device)
        parameters.optimizer.zero_grad()
        output = model(data)
        loss = parameters.criterion(output, target)
        loss.backward()
        parameters.optimizer.step()
        train_loss += loss.item()
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        pbar.set_description(desc=f'Train Loss={train_loss/len(parameters.train_loader.dataset):.4f}'+
                                  f'|Batch_id={batch_idx}'+
                                  f'|Accuracy={correct / len(parameters.train_loader.dataset):.2f}')
    train_loss /= len(parameters.train_loader.dataset)
    accuracy = 100. * correct / len(parameters.train_loader.dataset)
    return train_loss, accuracy, model  


def executar(lotes):
    """Treina por uma epoca. Ponto de entrada publico desta unidade.

    lotes: lista de  (amostras, rotulos); cada amostra tem um score por classe.
    Devolve (perda, acuracia, vies final do modelo, modelo em modo de treino).
    """
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    parameters = ParameterObject("cpu", loader, _Otimizador(modelo), _Perda)
    perda, acuracia, modelo = train(modelo, parameters)
    return perda, acuracia, modelo.vies, modelo.training
