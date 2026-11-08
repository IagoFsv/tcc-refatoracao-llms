from dataclasses import dataclass, asdict

@dataclass
class TreinamentoConfig:
    device: str
    criterion: nn.Module

@dataclass
class TreinamentoResult:
    train_loss: float
    accuracy: float
    model: _Modelo

def train(
        model: nn.modules,
        train_loader: DataLoader,
        optimizer: optim.Optimizer,
        config: TreinamentoConfig
        ) -> TreinamentoResult:
    model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(config.device), target.to(config.device)
        optimizer.zero_grad()
        output = model(data)
        loss = config.criterion(output, target)
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
    return TreinamentoResult(train_loss, accuracy, model)

def executar(lotes):
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    config = TreinamentoConfig(device="cpu", criterion=_Perda)
    result = train(modelo, loader, _Otimizador(modelo), config)
    return result.train_loss, result.accuracy, result.model.vies, result.model.training
