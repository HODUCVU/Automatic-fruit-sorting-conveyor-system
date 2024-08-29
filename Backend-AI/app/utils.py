import torch 
from torchvision import models
from torchvision import transforms
# from .app import utils
# from PIL import Image 
# from pathlib import Path

class modules():
  def __init__(self, model_path: str) -> None:
    self.transform = transforms.Compose([
      transforms.Resize(256),
      transforms.CenterCrop(224),
      transforms.ToTensor()
    ])
    self.classes = ['apple', 'orange']
    self.model = self.mobileNet_v2(self.classes, model_path)
    
  def mobileNet_v2(self, classes, model_path, device='cpu'):
    weights = models.MobileNet_V2_Weights.DEFAULT
    model_mobilenet_v2 = models.mobilenet_v2(weights=weights)
    num_ftrs = model_mobilenet_v2.classifier[1].in_features
    model_mobilenet_v2.classifier[1] = torch.nn.Linear(num_ftrs, len(classes))
    model_mobilenet_v2.load_state_dict(torch.load(model_path))
    model_mobilenet_v2.to(device)
    return model_mobilenet_v2
  
  def make_predict(self, image, device='cpu'):
    self.model.eval()
    transformed_image = self.transform(image).unsqueeze(0).to(device)
    self.model.to(device)
    with torch.inference_mode():
      y_pred = self.model(transformed_image)
      cls_to_idx = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
    return cls_to_idx