"""Uma epoca de treino de um classificador.

Ponto de entrada publico: executar(lotes). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.

As pecas de treino (tensor, modelo, perda, otimizador, loader) sao versoes
minimas em Python puro. O modelo soma um vies por classe ao score de cada
amostra; a perda e quanto o maior score passa o score da classe certa.
"""

from types import SimpleNamespace

from tqdm import tqdm

_NUM_CLASSES = 3
_TAXA_APRENDIZADO = 0.5


class _Tensor:
    """Tensor sobre listas: 1D (valores) ou 2D (uma linha por amostra)."""

    def __init__(self, valores, modelo=None):
        self.valores = valores
        self.modelo = modelo

    def to(self, device):
        return self

    def argmax(self, dim, keepdim):
        return _Tensor([[linha.index(max(linha))] for linha in self.valores])

    def view_as(self, outro):
        return _Tensor([[valor] for valor in self.valores])

    def eq(self, outro):
        return _Tensor([a == b for a, b in zip(self.valores, outro.valores)])

    def sum(self):
        return _Tensor(sum(self.valores))

    def item(self):
        return self.valores


class _Modelo:
    """Um vies por classe, somado ao score de cada amostra."""

    def __init__(self):
        self.vies = [0.0] * _NUM_CLASSES
        self.grad = [0.0] * _NUM_CLASSES
        self.training = False

    def train(self):
        self.training = True
        return self

    def __call__(self, data):
        linhas = [_somar(amostra, self.vies) for amostra in data.valores]
        return _Tensor(linhas, modelo=self)


def _somar(a, b):
    return [x + y for x, y in zip(a, b)]


class _Perda:
    """Media, no lote, de quanto o maior score passa o da classe certa."""

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


class _Otimizador:
    """Descida de gradiente sobre o vies do modelo."""

    def __init__(self, modelo):
        self.modelo = modelo

    def zero_grad(self):
        self.modelo.grad[:] = [0.0] * _NUM_CLASSES

    def step(self):
        passo = [_TAXA_APRENDIZADO * g for g in self.modelo.grad]
        self.modelo.vies = [b - p for b, p in zip(self.modelo.vies, passo)]


class DataLoader:
    """Itera sobre lotes (data, target) ja montados."""

    def __init__(self, lotes):
        self.lotes = lotes
        self.dataset = [amostra for data, _ in lotes for amostra in data.valores]

    def __iter__(self):
        return iter(self.lotes)

    def __len__(self):
        return len(self.lotes)


torch = SimpleNamespace(device=str)
nn = SimpleNamespace(Module=_Modelo, modules=_Modelo)
optim = SimpleNamespace(Optimizer=_Otimizador)


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
    # train_loss /= len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)
    accuracy = 100. * correct / len(train_loader.dataset)
    return train_loss, accuracy, model  


def executar(lotes):
    """Treina por uma epoca. Ponto de entrada publico desta unidade.

    lotes: lista de (amostras, rotulos); cada amostra tem um score por classe.
    Devolve (perda, acuracia, vies final do modelo, modelo em modo de treino).
    """
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    perda, acuracia, modelo = train(modelo, "cpu", loader, _Otimizador(modelo), _Perda)
    return perda, acuracia, modelo.vies, modelo.training
