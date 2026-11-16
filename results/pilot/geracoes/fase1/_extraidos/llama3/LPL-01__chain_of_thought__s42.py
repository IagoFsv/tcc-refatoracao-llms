class TrainConfig:
    def __init__(self, device, train_loader, optimizer, criterion):
        self.device = device
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion

def train(config: TrainConfig) -> tuple[float, float, nn.Module]:
    model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(config.train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(config.device), target.to(config.device)
        config.optimizer.zero_grad()
        output = model(data)
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
    return train_loss, accuracy, model

def executar(lotes):
    config = TrainConfig("cpu", DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes]), _Otimizador(_Modelo()), _Perda)
    perda, acuracia, modelo = train(config)
    return perda, acuracia, modelo.vies, modelo.training
