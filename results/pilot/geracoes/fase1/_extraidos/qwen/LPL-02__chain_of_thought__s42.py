from dataclasses import dataclass

@dataclass
class TreinoConfig:
    lotes: list
    device: str = "cpu"
    learning_rate: float = _TAXA_APRENDIZADO
    num_classes: int = _NUM_CLASSES

class DataLoader:
    """Itera sobre lotes (data, target) ja montados."""

    def __init__(self, lotes):
        self.lotes = lotes
        self.dataset = [amostra for data, _ in lotes for amostra in data.valores]

    def __iter__(self):
        return iter(self.lotes)

    def __len__(self):
        return len(self.lotes)


def train(
        model:nn.modules,
        device:torch.device, 
        train_loader: DataLoader, 
        optimizer:optim.Optimizer, 
        criterion: nn.Module
        )->tuple[float, float, nn.Module]:
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

    config: objeto de configuração com as informações necessárias para o treinamento.
    Devolve (perda, acuracia, vies final do modelo, modelo em modo de treino).
    """
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in config.lotes])
    perda, acuracia, modelo = train(modelo, config.device, loader, _Otimizador(modelo), _Perda)
    return perda, acuracia, modelo.vies, modelo.training
