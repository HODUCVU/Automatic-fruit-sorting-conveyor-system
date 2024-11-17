import cv2
from predict2 import Modules
import urllib.request
import numpy as np
import requests
from PIL import Image
import threading
cam_url = 'http://192.168.1.12'
url_monitor = f'{cam_url}/cam-hi.jpg'
url_predict = f'{cam_url}/cam-mid.jpg'

im = None
model = Modules('mobilenet_v2_model.pth')

def stream():
    # Stream images and display using OpenCV
    cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
    while True:
        img_resp = urllib.request.urlopen(url_monitor)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)

        cv2.imshow('live transmission', im)
        key = cv2.waitKey(5)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()

def predict():
    while True:
        try:
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
            url_server = 'https://cbf2-34-57-250-173.ngrok-free.app/'
            response = requests.post(f'{url_server}upload', json=data)
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                print("Prediction successfully posted!")
            else:
                print(f"Error posting prediction: {response.text}")
        except Exception as e:
            print(f"Error in predict function: {e}")

if __name__ == '__main__':
    print("started")

    # Run streaming and prediction concurrently in separate threads
    stream_thread = threading.Thread(target=stream)
    predict_thread = threading.Thread(target=predict)

    stream_thread.start()
    predict_thread.start()

    stream_thread.join()
    predict_thread.join()