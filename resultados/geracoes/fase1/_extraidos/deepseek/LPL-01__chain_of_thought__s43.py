from types import SimpleNamespace
from tqdm import tqdm

_NUM_CLASSES = 3
_TAXA_APRENDIZADO = 0.5

class Params:
    def __init__(self, device, train_loader, optimizer, criterion):
        self.device = device
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion

class  _Tensor:
    # ... restante do código ...

class _Modelo:
    # ... restante do código ...

def _somar(a, b):
    return [x + y for x, y in zip(a, b)]

class _Perda:
    # ... restante do código ...

class _Otimizador:
    # ... restante do código ...

class DataLoader:
    # ... restante do código ...

torch = SimpleNamespace(device=str)
nn = SimpleNamespace(Module=_Modelo, modules=_Modelo)
optim = SimpleNamespace(Optimizer=_Otimizador)


def train(params: Params, model:nn.modules) -> tuple[float, float, nn.Module]:
    '''
    basic train function generate by github-copilot
    args
        params: Params object that contains all the necessary information for training
        model: model to train
    return
        train_loss: loss of the training process
        accuracy: accuracy of the training process
        model: trained model
    '''
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
    params = Params("cpu", loader, _Otimizador(modelo), _Perda)
    perda, acuracia, modelo = train(params, modelo)
    return perda, acuracia, modelo.vies, modelo.training
