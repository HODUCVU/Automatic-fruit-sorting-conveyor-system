import cv2
from predict import Modules
import urllib.request
import numpy as np
import requests
from PIL import Image

url_server = 'https://c014-34-138-212-26.ngrok-free.app/upload'
cam_url = 'https://hot-longhorn-actively.ngrok-free.app/cam-hi.jpg'
im=None
model = Modules('mobilenet_v2_model.pth')
        
def predict():
    while True:
        try:
            # print("Attempting to access the camera feed...")
            # Get image from the camera feed
            img_resp = urllib.request.urlopen(cam_url)
            # print("Request success\n")
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            im = cv2.imdecode(imgnp, -1)
            # print("Read image\n")
            pre = model.make_predict(im)
            print(f"Predict: {pre}")

            # Prepare the data to send
            data = {
                "prediction": pre, 
                "status": "200"
            }
            # Make a POST request to send the prediction to the API
            # print("Posting to server...\n")
            response = requests.post(f'{url_server}', json=data, timeout=10)
            # print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                print("Prediction successfully posted!")
            else:
                print(f"Error posting prediction: {response.text}")
        except Exception as e:
            print(f"Error in predict function: {e}")

if __name__ == '__main__':
    print("started")
    predict()