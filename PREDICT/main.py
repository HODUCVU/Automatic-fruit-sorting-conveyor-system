import cv2
from predict import Modules
import urllib.request
import numpy as np
# import concurrent.futures
import requests
from PIL import Image

# cam_url = 'http://192.168.1.12'
cam_url = 'https://7806-2001-ee0-4b42-8000-eb02-5b99-739f-3543.ngrok-free.app'
url_server = 'https://cbf2-34-57-250-173.ngrok-free.app'

url_monitor=f'{cam_url}/cam-hi.jpg'
url_predict=f'{cam_url}/cam-mid.jpg'

im=None
model = Modules('mobilenet_v2_model.pth')
def stream():
    while True:
        img_resp=urllib.request.urlopen(url_monitor)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        im = cv2.imdecode(imgnp,-1)
 
        cv2.imshow('live transmission',im)
        key=cv2.waitKey(5)
        if key==ord('q'):
            break
            
    cv2.destroyAllWindows()
        
def predict():
    while True:
        try:
            # Get image from the camera feed
            img_resp = urllib.request.urlopen(url_predict)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            im = cv2.imdecode(imgnp, -1)

            pre = model.make_predict(im)
            print(f"Predict: {pre}")

            # Prepare the data to send
            data = {
                "prediction": pre, 
                "status": "success"
            }
            # Make a POST request to send the prediction to the API
            response = requests.post(f'{url_server}/upload', json=data)
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                print("Prediction successfully posted!")
            else:
                print(f"Error posting prediction: {response.text}")
            # except requests.exceptions.RequestException as e:
            #     print(f"Error during request: {e}")
        except Exception as e:
            print(f"Error in predict function: {e}")

        # Check for quit key
        key = cv2.waitKey(5)
        if key == ord('q'):
            break
 
 
if __name__ == '__main__':
    print("started")
    predict()
