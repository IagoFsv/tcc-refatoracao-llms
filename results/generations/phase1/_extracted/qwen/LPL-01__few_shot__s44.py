from dataclasses import dataclass, asdict

@dataclass
class TrainingParameters:
    device: str
    train_loader: DataLoader
    optimizer: _Optimizer
    criterion: nn.Module

@dataclass
class TrainResults:
    train_loss: float
    accuracy: float
    model: _Model
    training_mode: bool

def train(
        model: _Model,
        parameters: TrainingParameters
) -> TrainResults:
    model.train()
    train_loss = 0
    correct = 0
    pbar = tqdm(parameters.train_loader)
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(parameters.device), target.to(parameters.device)
        parameters.optimizer.zero_grad()
        output = model(data)
        loss = parameters.criterion(output, target)
        loss.backward()
        parameters.optimizer.step()
        train_loss += loss.item()
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        pbar.set_description(desc=f'Train Loss={train_loss/len(parameters.train_loader.dataset ):.4f}'+
                                  f'|Batch_id={batch_idx}'+
                                  f'|Accuracy={correct / len(parameters.train_loader.dataset):.2f}')
    train_loss /= len(parameters.train_loader.dataset)
    accuracy = 100. * correct / len(parameters.train_loader.dataset)
    return TrainResults(train_loss, accuracy, model, model.training)


def run(batches):
    """Trains for one epoch. Public entry point of this unit.

    batches: list of (samples, labels); each sample has one score per class.
    Returns (loss, accuracy, final model bias, whether the model is in training mode).
    """
    model = _Model()
    loader = DataLoader([(_Tensor(s), _Tensor(l)) for s, l in batches])
    parameters = TrainingParameters(device="cpu", train_loader=loader, optimizer=_Optimizer(model), criterion=_Loss)
    results = train(model, parameters)
    return results.train_loss, results.accuracy, results.model.bias, results.training_mode
