from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from pathlib import Path
from PIL import Image
# import matplotlib.pyplot as plt

from utils import modules


router = APIRouter(
    prefix='/predict',
    tags=['Prediction']
)
# Test 
model = modules('models/mobilenet_v2_model.pth')

image_dir = [Path('test_inputs/input_1.png')]

IMAGEDIR = "test_inputs/"

import time
def clean_memory(image_dir):
    while True:
        # how many images in store
        files = []
        for _, _, filenames in os.walk(IMAGEDIR):
            for filename in filenames:
                files.append(os.path.join(IMAGEDIR, filename))
        # clean memory
        if len(files) >= 30: # 1s video has 30 frames 
            for file in files:
                if os.path.exists(file):
                    os.remove(file)
            print("Cleaned memory")
            del files
            del image_dir[:-1]
        # wait for 2s before checking again
        time.sleep(2)
import threading
def start_clean_memory_in_background():
    thread = threading.Thread(target=clean_memory, args=(image_dir,))
    # Allows the thread to close when the main program exits
    thread.setDaemon(True)    
    thread.start()

# # Initialize the background task when the FastAPI app starts
@router.on_event("startup")
def start_event():
    start_clean_memory_in_background()
    print("Started background task")


# from typing import Annotated
# @router.post("/esp32cam")
# async def create_image(file: Annotated[bytes, File()]):
#     return {"File_size": len(file)}

import os
@router.get('/', status_code=status.HTTP_200_OK)
def get_predictions():
    image = Image.open(image_dir[-1])
    pred = model.make_predict(image)
    return {"message": model.classes[pred]}

import uuid
@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file.filename = f'{uuid.uuid4()}.jpg'
    contents = await file.read()
    
    image_dir.append(Path(f'{IMAGEDIR}{file.filename}'))
    image_dir[-1].parent.mkdir(parents=True, exist_ok=True)
    with open(image_dir[-1], 'wb') as f:
        f.write(contents)
    return {"Uploaded": image_dir[-1]}

# ===================
#  Stream video
