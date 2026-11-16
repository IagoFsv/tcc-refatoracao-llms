from dataclasses import dataclass, asdict

@dataclass
class Treinamento:
    device: str
    train_loader: DataLoader
    optimizer: _Otimizador
    criterion: _Perda

def train(modelo: _Modelo, treinamento: Treinamento) -> tuple[float, float, _Modelo]:
    modelo.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(treinamento.train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(treinamento.device), target.to(treinamento.device)
        treinamento.optimizer.zero_grad()
        output = modelo(data)
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
    return train_loss, accuracy, modelo

def executar(lotes):
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    treinamento = Treinamento("cpu", loader, _Otimizador(modelo), _Perda)
    perda, acuracia, modelo = train(modelo, treinamento)
    return perda, acuracia, modelo.vies, modelo.training
