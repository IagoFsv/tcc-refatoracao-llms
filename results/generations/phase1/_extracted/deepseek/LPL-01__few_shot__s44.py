from dataclasses import dataclass, asdict
from types import SimpleNamespace
from tqdm import tqdm

_NUM_CLASSES = 3
_LEARNING_RATE = 0.5


class _Tensor:
    """Tensor over lists: 1D (values) or 2D (one row per sample)."""

    def __init__(self, values, model=None):
        self.values = values
        self.model = model

    def to(self, device):
        return self

    def argmax(self, dim, keepdim):
        return _Tensor([[row.index(max(row))] for row in self.values])

    def view_as(self, other):
        return _Tensor([[value] for value in self.values])

    def eq(self, other):
        return _Tensor([a == b for a, b in zip(self.values, other.values)])

    def sum(self):
        return _Tensor(sum(self.values))

    def item(self):
        return self.values


class _Model:
    """One bias per class, added to the score of each sample."""

    def __init__(self):
        self.bias = [0.0] * _NUM_CLASSES
        self.grad = [0.0] * _NUM_CLASSES
        self.training = False

    def train(self):
        self.training = True
        return self

    def __call__(self, data):
        rows = [self._add(sample, self.bias) for sample in data.values]
        return _Tensor(rows, model=self)

    def _add(self, a, b):
        return [x + y for x, y in zip(a, b)]


class _Loss:
    """Batch mean of how much the highest score exceeds the correct class score."""

    def __init__(self, output, target):
        self.output = output
        self.pairs = list(zip(output.values, target.values))

    def item(self):
        return sum(max(row) - row[label] for row, label in self.pairs) / len(self.pairs)

    def backward(self):
        grad = self.output.model.grad
        for row, label in self.pairs:
            grad[row.index(max(row))] += 1 / len(self.pairs)
            grad[label] -= 1 / len(self.pairs)


class _Optimizer:
    """Gradient descent on the model bias."""

    def __init__(self, model):
        self.model = model

    def zero_grad(self):
        self.model.grad[:] = [0.0] * _NUM_CLASSES

    def step(self):
        delta = [self._LEARNING_RATE * g for g in self.model.grad]
        self.model.bias = [b - d for b, d in zip(self.model.bias, delta)]


class DataLoader:
    """Iterates over ready-made (data, target) batches."""

    def __init__(self, batches):
        self.batches = batches
        self.dataset = [sample for data, _ in batches for sample in data.values]

    def __iter__(self):
        return iter(self.batches)

    def __len__(self):
        return len(self.batches)


torch = SimpleNamespace(device=str)
nn = SimpleNamespace(Module=_Model, modules=_Model)
optim = SimpleNamespace(Optimizer=_Optimizer)


def train(
        model:nn.modules,
        device:torch.device, 
        train_loader: DataLoader, 
        optimizer:optim.Optimizer, 
        criterion: nn.Module
        
)->tuple[float, float, nn.Module]:

    model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(train_loader)
    for batch_idx,  (data, target) in enumerate(pbar):
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
                                  f'|Accuracy={correct  / len(train_loader.dataset):.2f}')
    train_loss /= len(train_loader.dataset)
    accuracy = 100. * correct / len(train_loader.dataset)
    return train_loss, accuracy, model  


def run(batches):

    model = _Model()
    loader = DataLoader([(_Tensor(s), _Tensor(l)) for s, l in batches])
    loss, accuracy, model = train(model, "cpu", loader, _Optimizer(model), _Loss)
    return loss, accuracy, model.bias, model.training
