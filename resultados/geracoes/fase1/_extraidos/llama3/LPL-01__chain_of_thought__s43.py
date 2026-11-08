from types import SimpleNamespace

from tqdm import tqdm

_NUM_CLASSES = 3
_TAXA_APRENDIZADO = 0.5


class _Tensor:
    # ...

class _Modelo:
    # ...

class _Perda:
    # ...

class _Otimizador:
    # ...

class DataLoader:
    # ...

torch = SimpleNamespace(device=str)
nn = SimpleNamespace(Module=_Modelo, modules=_Modelo)
optim = SimpleNamespace(Optimizer=_Otimizador)


class Treinamento:
    def __init__(self, device, train_loader, optimizer, criterion):
        self.device = device
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion


def train(model, treinamento):
    model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(treinamento.train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(treinamento.device), target.to(treinamento.device)
        treinamento.optimizer.zero_grad()
        output = model(data)
        loss = treinamento.criterion(output, target)
        loss.backward()
        treinamento.optimizer.step()
        train_loss += loss.item()
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        pbar.set_description(desc=f'Train Loss={train_loss/len(treinamento.train_loader.dataset ):.4f}'+
                                  f'|Batch_id={batch_idx}'+
                                  f'|Accuracy={correct / len(treinamento.train_loader.dataset):.2f}')
    train_loss /= len(treinamento.train_loader.dataset)
    accuracy = 100. * correct / len(treinamento.train_loader.dataset)
    return train_loss, accuracy, model


def executar(lotes):
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    treinamento = Treinamento("cpu", loader, _Otimizador(modelo), _Perda())
    perda, acuracia, modelo = train(modelo, treinamento)
    return perda, acuracia, modelo.vies, modelo.training
