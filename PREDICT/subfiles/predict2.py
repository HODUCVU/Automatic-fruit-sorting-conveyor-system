import torch
import os
from torchvision import models, transforms
from PIL import Image
import numpy as np

class Modules:
    def __init__(self, model_path: str, device: str = 'cpu') -> None:
        self.device = device
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor()
        ])
        self.classes = ['RedApple', 'GreenApple']
        self.model = self.mobileNet_v2(model_path=model_path)

    def mobileNet_v2(self, model_path, device='cpu'):
        weights = models.MobileNet_V2_Weights.DEFAULT
        model_mobilenet_v2 = models.mobilenet_v2(weights=weights)
        num_ftrs = model_mobilenet_v2.classifier[1].in_features
        model_mobilenet_v2.classifier[1] = torch.nn.Linear(num_ftrs, 2)
        model_mobilenet_v2.load_state_dict(torch.load(model_path, weights_only=True))
        model_mobilenet_v2.to(device)
        return model_mobilenet_v2

    def make_predict(self, image):
        try:
            self.model.to(self.device)
            self.model.eval()

            # Ensure input image is PIL and RGB format
            if isinstance(image, np.ndarray):
                # print(f"Image shape: {image.shape}, dtype: {image.dtype}")
                image = Image.fromarray(image)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            # print(f"Image mode after conversion: {image.mode}")

            # Transform image
            # # print("Starting transformation steps...")
            # resized_image = transforms.Resize(256)(image)
            # # print("Resize successful")
            # cropped_image = transforms.CenterCrop(224)(resized_image)
            # # print("Center crop successful")
            
            # # Convert to tensor manually
            # tensor_image = torch.from_numpy(np.array(cropped_image)).permute(2, 0, 1).float() / 255.0
            # # print("Manual ToTensor conversion successful")
            # # print(f"Tensor shape: {tensor_image.shape}, dtype: {tensor_image.dtype}")

            # # Add batch dimension
            # transformed_image = tensor_image.unsqueeze(0).to(self.device)
            # # print("Image transformed and ready for prediction")
            transformed_image = self.transform(image).unsqueeze(0).to(self.device)
            # Perform prediction
            with torch.inference_mode():
                y_pred = self.model(transformed_image)
                cls_to_idx = torch.argmax(torch.softmax(y_pred, dim=1), dim=1).item()
                return self.classes[cls_to_idx]

        except Exception as e:
            print(f"Error during prediction: {e}")
            return None

if __name__ == '__main__':
    model = Modules('mobilenet_v2_model.pth')
    # Example usage with an image path
    image = Image.open("a2.jpeg")
    prediction = model.make_predict(image)
    print(f"Prediction: {prediction}")
    image = Image.open("a1.jpeg")
    prediction = model.make_predict(image)
    print(f"Prediction: {prediction}")
