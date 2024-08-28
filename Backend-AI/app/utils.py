import torch
def make_predict(model, image, transform, device='cpu'):
  model.eval()
  transformed_image = transform(image).unsqueeze(0).to(device)
  model.to(device)
  with torch.inference_mode():
    y_pred = model(transformed_image)
    cls_to_idx = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
  return cls_to_idx

class_name = ['apple', 'orange']
