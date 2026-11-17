from dataclasses import dataclass, asdict

@dataclass
class TrainingParameters:
    device: str
    train_loader: DataLoader
    optimizer: optim.Optimizer
    criterion: nn.Module

@dataclass
class TrainingResults:
    train_loss: float
    accuracy: float
    model_bias: list
    model_training_mode: bool

def train(
        model: nn.modules,
        parameters: TrainingParameters
        ) -> TrainingResults:
    '''
    basic train function generate by github-copilot
    args
        model: model to train
        parameters: training parameters
    return
        train_loss: loss of the training process
        accuracy: accuracy of the training process
        model_bias: trained model bias
        model_training_mode: whether the model is in training mode
    '''
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
    return TrainingResults(train_loss, accuracy, model.bias, model.training)


def run(batches):
    """Trains for one epoch. Public entry point of this unit.

    batches: list of (samples, labels); each sample has one score per class.
    Returns (loss, accuracy, final model bias, whether the model is in training mode).
    """
    model = _Model()
    loader = DataLoader([(_Tensor(s), _Tensor(l)) for s, l in batches])
    parameters = TrainingParameters("cpu", loader, _Optimizer(model), _Loss)
    results = train(model, parameters)
    return results.train_loss, results.accuracy, results.model_bias, results.model_training_mode
