class TrainParameters:
    def __init__(self, model: nn.modules, device: torch.device, train_loader: DataLoader, 
                 optimizer: optim.Optimizer, criterion: nn.Module):
        self.model = model
        self.device = device
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion

def train(params: TrainParameters)->tuple[float, float, nn.Module]:
    '''
    basic train function generate by github-copilot
    args
        device: device to train the model
        train_loader: training data loader
        optimizer: optimizer for the model
        criterion: loss function    
    return
        train_loss: loss of the training process
        accuracy: accuracy of the training process
        model: trained model
    '''
    model = params.model
    model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(params.train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(params.device), target.to(params.device)
        params.optimizer.zero_grad()
        output = model(data)
        loss = params.criterion(output, target)
        loss.backward()
        params.optimizer.step()
        train_loss += loss.item()
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        pbar.set_description(desc=f'Train Loss={train_loss/len(params.train_loader.dataset):.4f}'+
                                  f'|Batch_id={batch_idx}'+
                                  f'|Accuracy={correct / len(params.train_loader.dataset):.2f}')
    train_loss /= len(params.train_loader.dataset)
    accuracy = 100. * correct / len(params.train_loader.dataset)
    return train_loss, accuracy, model

def executar(lotes):
    """Treina por uma epoca. Ponto de entrada publico desta unidade.
    lotes: lista de  (amostras, rotulos); cada amostra tem um score por classe.
    Devolve (perda, acuracia, vies final do modelo, modelo em modo de treino).
    """
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    params = TrainParameters(modelo, "cpu", loader, _Otimizador(modelo), _Perda)
    perda, acuracia, modelo = train(params)
    return perda, acuracia, modelo.vies, modelo.training
