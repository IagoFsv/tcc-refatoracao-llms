from dataclasses import dataclass

@dataclass
class TreinoConfig:
    lotes: list
    device: str = "cpu"
    otimizador: '_Otimizador' = None
    perda: '_Perda' = None

def train(
        model: nn.modules,
        device: torch.device,
        train_loader: DataLoader,
        optimizer: optim.Optimizer,
        criterion: nn.Module
) -> tuple[float, float, nn.Module]:
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
    model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        pbar.set_description(desc=f'Train Loss={train_loss/len(train_loader.dataset ):.4f}'+
                                  f'|Batch_id={batch_idx}'+
                                  f'|Accuracy={correct / len(train_loader.dataset):.2f}')
    train_loss /= len(train_loader.dataset)
    accuracy = 100. * correct / len(train_loader.dataset)
    return train_loss, accuracy, model  


def executar(config: TreinoConfig):
    """Treina por uma epoca. Ponto de entrada publico desta unidade.

    config: configuracao de treino
    Devolve (perda, acuracia, vies final do modelo, modelo em modo de treino).
    """
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in config.lotes])
    perda = config.perda or _Perda
    otimizador = config.otimizador or _Otimizador(modelo)
    train_loss, acuracia, modelo = train(modelo, config.device, loader, otimizador, perda)
    return train_loss, acuracia, modelo.vies, modelo.training
