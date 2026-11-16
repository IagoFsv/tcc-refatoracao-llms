from dataclasses import dataclass, asdict

@dataclass
class TreinamentoConfig:
    device: str
    taxa_aprendizado: float
    num_classes: int

@dataclass
class TreinamentoDados:
    lotes: list

@dataclass
class TreinamentoResultados:
    train_loss: float
    accuracy: float
    modelo: 'Modelo'

class Modelo:
    def __init__(self):
        self.vies = [0.0] * TreinamentoConfig.num_classes
        self.grad = [0.0] * TreinamentoConfig.num_classes
        self.training = False

    def train(self):
        self.training = True
        return self

    def __call__(self, data):
        linhas = [_somar(amostra, self.vies) for amostra in data.valores]
        return _Tensor(linhas, modelo=self)

def _somar(a, b):
    return [x + y for x, y in zip(a, b)]

class Perda:
    def __init__(self, output, target):
        self.output = output
        self.pares = list(zip(output.valores, target.valores))

    def item(self):
        return sum(max(linha) - linha[classe] for linha, classe in self.pares) / len(self.pares)

    def backward(self):
        grad = self.output.modelo.grad
        for linha, classe in self.pares:
            grad[linha.index(max(linha))] += 1 / len(self.pares)
            grad[classe] -= 1 / len(self.pares)

class Otimizador:
    def __init__(self, modelo):
        self.modelo = modelo

    def zero_grad(self):
        self.modelo.grad[:] = [0.0] * TreinamentoConfig.num_classes

    def step(self):
        passo = [TreinamentoConfig.taxa_aprendizado * g for g in self.modelo.grad]
        self.modelo.vies = [b - p for b, p in zip(self.modelo.vies, passo)]

class DataLoader:
    def __init__(self, lotes):
        self.lotes = lotes
        self.dataset = [amostra for data, _ in lotes for amostra in data.valores]

    def __iter__(self):
        return iter(self.lotes)

    def __len__(self):
        return len(self.lotes)

def train(modelo: Modelo, device: str, train_loader: DataLoader, optimizer: Otimizador, criterion: Perda) -> TreinamentoResultados:
    modelo.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = modelo(data)
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
    return TreinamentoResultados(train_loss, accuracy, modelo)

def executar(lotes):
    config = TreinamentoConfig(device="cpu", taxa_aprendizado=0.5, num_classes=3)
    TreinamentoConfig.num_classes = config.num_classes
    TreinamentoConfig.taxa_aprendizado = config.taxa_aprendizado
    TreinamentoConfig.device = config.device
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    perda, acuracia, modelo = train(Modelo(), config.device, loader, Otimizador(Modelo()), Perda)
    return perda, acuracia, modelo.vies, modelo.training
