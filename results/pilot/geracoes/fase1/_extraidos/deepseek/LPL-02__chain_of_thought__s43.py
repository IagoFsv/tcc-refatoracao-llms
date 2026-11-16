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

class _Tensor:
    # ... código omitido ...

class _Modelo:
    # ... código omitido ...

class _Perda:
    # ... código omitido ...

class _Otimizador:
    # ... código omitido ...

class DataLoader:
    # ... código omitido ...

torch = SimpleNamespace(device=str)
nn = SimpleNamespace(Module=_Modelo, modules=_Modelo)
optim = SimpleNamespace(Optimizer=_Otimizador)

def train(params: Params):
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
    model = params.train_loader.dataset[0][1].modelo
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

    lotes: lista de 2-tuplas (amostras, rotulos); cada amostra tem um score por classe.
    Devolve uma 4-tupla (perda, acuracia, vies final do modelo, modelo em modo de treino).
    """
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    perda, acuracia, modelo = train(Params("cpu", loader, _Otimizador(modelo), _Perda))
    return perda, acuracia, modelo.vies, modelo.training
