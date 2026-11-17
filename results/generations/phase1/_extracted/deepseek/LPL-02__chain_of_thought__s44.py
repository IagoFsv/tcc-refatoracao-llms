class TrainingParameters:
    def __init__(self, model, device, train_loader, optimizer, criterion):
        self.model = model
        self.device = device
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion

def train(params: TrainingParameters):
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
    model = params.model
    device = params.device
    train_loader = params.train_loader
    optimizer = params.optimizer
    criterion = params.criterion
    
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

    batches: list of  (samples, labels); each sample has one score per class.
    Returns (loss, accuracy, final model bias, whether the model is in training mode).
    """
    model = _Model()
    loader = DataLoader([(_Tensor(s), _Tensor(l)) for s, l in batches])
    params = TrainingParameters(model, "cpu", loader, _Optimizer(model), _Loss)
    loss, accuracy, model = train(params)
    return loss, accuracy, model.bias, model.training
