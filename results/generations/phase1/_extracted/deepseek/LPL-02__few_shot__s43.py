from types import SimpleNamespace
from tqdm import tqdm
from dataclasses import dataclass, asdict

_NUM_CLASSES = 3
_LEARNING_RATE = 0.5

@dataclass
class Sample:
    values: list
    model: '_Model' = None

@dataclass
class _Model:
    bias: list = None
    grad: list = None
    training: bool = False

    def train(self):
        self.training = True
        return self

    def __call__(self, data: Sample):
        rows = [_add(sample, self.bias) for sample in data.values]
        return Sample(rows, model=self)

def _add(a, b):
    return [x + y for x, y in zip(a, b)]

@dataclass
class _Loss:
    output: Sample
    pairs: list = None

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

@dataclass
class _Optimizer:
    model: _Model

    def zero_grad(self):
        self.model.grad[:] = [0.0] * _NUM_CLASSES

    def step(self):
        delta = [_LEARNING_RATE * g for g in self.model.grad]
        self.model.bias = [b - d for b, d in zip(self.model.bias, delta)]

@dataclass
class DataLoader:
    batches: list
    dataset: list = None

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
        pbar.set_description(desc=f'Train Loss={train_loss/len(train_loader.dataset):.4f}'+
                                  f'|Batch_id={batch_idx}'+
                                  f'|Accuracy={correct / len(train_loader.dataset):.2f}')
    train_loss /= len(train_loader.dataset)
    accuracy = 100. * correct / len(train_loader.dataset)
    return train_loss, accuracy, model  

def run(batches):
    """Trains for one epoch. Public entry point of this unit.
    batches: list of (samples, labels); each sample has one score per class.
    Returns (loss, accuracy, final model bias, whether the model is in training mode).
    """
    model = _Model()
    loader = DataLoader([(Sample(s), Sample(l)) for s, l in batches])
    loss, accuracy, model = train(model, "cpu", loader, _Optimizer(model), _Loss)
    return loss, accuracy, model.bias, model.training
