import torch 
import os
from torchvision import models
from torchvision import transforms
from PIL import Image
import numpy as np
class Modules():
  def __init__(self, model_path: str) -> None:
    self.transform = transforms.Compose([
      transforms.Resize(256),
      transforms.CenterCrop(224),
      transforms.ToTensor()
    ])
    self.classes = ['GreenApple', 'RedApple']
    
    # self.classes = ['RedApple','GreenApple']
    self.model = self.mobileNet_v2(model_path=model_path)
    
  def mobileNet_v2(self, model_path, device='cpu'):
    weights = models.MobileNet_V2_Weights.DEFAULT
    model_mobilenet_v2 = models.mobilenet_v2(weights=weights)
    num_ftrs = model_mobilenet_v2.classifier[1].in_features
    model_mobilenet_v2.classifier[1] = torch.nn.Linear(num_ftrs, 2)
    model_mobilenet_v2.load_state_dict(torch.load(model_path))
    model_mobilenet_v2.to(device)
    return model_mobilenet_v2
  
  def make_predict(self, image, device='cpu'):
    try:
        self.model.eval()
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        transformed_image = self.transform(image).unsqueeze(0).to(device)
        self.model.to(device)
        with torch.inference_mode():
            y_pred = self.model(transformed_image)
            cls_to_idx = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
            return self.classes[cls_to_idx]
    except KeyError:
        print("error\n")
        return None

if __name__ == '__main__':
  model = Modules('mobilenet_v2_model.pth')
  from PIL import Image
  image = Image.open('a1.jpeg')
  pred = model.make_predict(image)
  print(pred)
  image = Image.open('a2.jpeg')
  pred = model.make_predict(image)
  print(pred)