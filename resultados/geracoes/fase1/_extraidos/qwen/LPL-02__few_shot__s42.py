from dataclasses import dataclass, asdict

@dataclass
class TreinamentoConfig:
    device: str = "cpu"
    taxa_aprendizado: float = 0.5
    num_classes: int = 3

@dataclass
class Tensor:
    valores: list
    modelo: 'Modelo' = None

    def to(self, device):
        return self

    def argmax(self, dim, keepdim):
        return Tensor([[linha.index(max(linha))] for linha in self.valores])

    def view_as(self, outro):
        return Tensor([[valor] for valor in self.valores])

    def eq(self, outro):
        return Tensor([a == b for a, b in zip(self.valores, outro.valores)])

    def sum(self):
        return Tensor(sum(self.valores))

    def item(self):
        return self.valores

@dataclass
class Modelo:
    vies: list = None
    grad: list = None
    training: bool = False

    def train(self):
        self.training = True
        return self

    def __call__(self, data):
        linhas = [_somar(amostra, self.vies) for amostra in data.valores]
        return Tensor(linhas, modelo=self)

def _somar(a, b):
    return [x + y for x, y in zip(a, b)]

@dataclass
class Perda:
    output: Tensor
    target: Tensor

    def item(self):
        return sum(max(linha) - linha[classe] for linha, classe in zip(self.output.valores, self.target.valores)) / len(self.pares)

    def backward(self):
        grad = self.output.modelo.grad
        for linha, classe in zip(self.output.valores, self.target.valores):
            grad[linha.index(max(linha))] += 1 / len(self.pares)
            grad[classe] -= 1 / len(self.pares)

@dataclass
class Otimizador:
    modelo: Modelo

    def zero_grad(self):
        self.modelo.grad[:] = [0.0] * self.modelo.num_classes

    def step(self):
        passo = [self.modelo.taxa_aprendizado * g for g in self.modelo.grad]
        self.modelo.vies = [b - p for b, p in zip(self.modelo.vies, passo)]

class DataLoader:
    def __init__(self, lotes):
        self.lotes = lotes
        self.dataset = [amostra for data, _ in lotes for amostra in data.valores]

    def __iter__(self):
        return iter(self.lotes)

    def __len__(self):
        return len(self.lotes)

def train(
        model: Modelo,
        config: TreinamentoConfig,
        train_loader: DataLoader,
        optimizer: Otimizador,
        criterion: Perda
) -> tuple[float, float, Modelo]:
    model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(config.device), target.to(config.device)
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

def executar(lotes):
    config = TreinamentoConfig()
    modelo = Modelo(vies=[0.0] * config.num_classes, taxa_aprendizado=config.taxa_aprendizado)
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    perda = Perda(output=modelo, target=None)
    optimizer = Otimizador(modelo=modelo)
    train_loss, accuracy, modelo = train(modelo, config, loader, optimizer, perda)
    return train_loss, accuracy, modelo.vies, modelo.training
