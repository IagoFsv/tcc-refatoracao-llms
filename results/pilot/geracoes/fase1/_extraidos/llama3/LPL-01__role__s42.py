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

class TrainingConfig:
    def __init__(self, model, device, train_loader, optimizer, criterion):
        self.model = model
        self.device = device
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion

def train(config: TrainingConfig) -> tuple[float, float, _Modelo]:
    config.model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(config.train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(config.device), target.to(config.device)
        config.optimizer.zero_grad()
        output = config.model(data)
        loss = config.criterion(output, target)
        loss.backward()
        config.optimizer.step()
        train_loss += loss.item()
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        pbar.set_description(desc=f'Train Loss={train_loss/len(config.train_loader.dataset ):.4f}'+
                                  f'|Batch_id={batch_idx}'+
                                  f'|Accuracy={correct / len(config.train_loader.dataset):.2f}')
    train_loss /= len(config.train_loader.dataset)
    accuracy = 100. * correct / len(config.train_loader.dataset)
    return train_loss, accuracy, config.model

def executar(lotes):
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    config = TrainingConfig(modelo, "cpu", loader, _Otimizador(modelo), _Perda())
    perda, acuracia, modelo = train(config)
    return perda, acuracia, modelo.vies, modelo.training
