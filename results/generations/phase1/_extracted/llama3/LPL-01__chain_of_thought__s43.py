class TrainingConfig:
    def __init__(self, model, device, optimizer, criterion):
        self.model = model
        self.device = device
        self.optimizer = optimizer
        self.criterion = criterion

def train(config: TrainingConfig) -> tuple[float, float, nn.Module]:
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

def run(batches):
    model = _Model()
    loader = DataLoader([(_Tensor(s), _Tensor(l)) for s, l in batches])
    config = TrainingConfig(model, "cpu", _Optimizer(model), _Loss)
    loss, accuracy, model = train(config)
    return loss, accuracy, model.bias, model.training
