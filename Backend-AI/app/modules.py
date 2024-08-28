import torch 
from torch import nn 
from torchvision import models

def mobileNet_v2(classes, device='cuda' if torch.cuda.is_available() else 'cpu'):
    weights = models.MobileNet_V2_Weights.DEFAULT
    model_mobilenet_v2 = models.mobilenet_v2(weights=weights)
    num_ftrs = model_mobilenet_v2.classifier[1].in_features
    model_mobilenet_v2.classifier[1] = torch.nn.Linear(num_ftrs, classes)
    model_mobilenet_v2.load_state_dict(torch.load('./models/mobilenet_v2_model.pth'))
    model_mobilenet_v2.to(device)
    return model_mobilenet_v2

