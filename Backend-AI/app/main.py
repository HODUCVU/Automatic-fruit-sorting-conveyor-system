# RUN FASTAPI FROM WSL
# https://smartshock.hashnode.dev/port-forwarding-from-ubuntu-wsl-to-windows-host#heading-step-2-find-the-ip-address-of-ubuntu-wsl

# uvicorn app.main:app --reload   
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# run on http://127.0.0.1:8000/
# python main.py

# check active portL `isof -i:8000`
#  kill port: kill -9 <PID>

# import io
from fastapi import FastAPI, status, UploadFile, BackgroundTasks
from PIL import Image
from app.utils import modules
import uuid
import shutil
import os
import logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

model = modules('app/models/mobilenet_v2_model.pth')


IMAGEDIR = "app/images/"
os.makedirs(IMAGEDIR, exist_ok=True)
image_dir = []

def save_image(file: UploadFile):
    """Upload an image and trigger background tasks for cleanup."""
    global image_dir
    
    file.filename = f'{uuid.uuid4()}.jpg'
    image_path = os.path.join(IMAGEDIR, file.filename)
    logging.info(f"Starting to save the image: {file.filename}")
    try:
        if file.size > 2 * 1024 * 1024:
            return {"Message": "File too large"}
        # Save image
        with open(image_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        image_dir.append(image_path)
        
        logging.info(f"Image saved in {image_path}")
        logging.info(f"File size after saving: {os.path.getsize(image_path)}")
        
    except Exception as e:
        logging.error(f"Error saving image: {e}")
    finally:
        file.file.seek(0)    

def cleanup_images():
    global image_dir
    logging.info("Start cleaning images...")
    if len(image_dir) > 30:
        for img_path in image_dir[:-5]:
            if os.path.exists(img_path):
                os.remove(img_path)
        image_dir = image_dir[-5:]
        logging.info("Cleaned up old images")

@app.get('/', status_code=status.HTTP_200_OK)
async def get_predictions():
    """Get predictions for the latest image."""
    if not image_dir:
        return {"Message": "No image found"}
    try:
        image = Image.open(image_dir[-1])
        pred = model.make_predict(image)
        return {"message": model.classes[pred]}
    except Exception as e:
        logging.info(f"Error prediction: {e}")
        return {"message": e}
        

@app.post('/', status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile, background_tasks: BackgroundTasks):
    save_image(file)
    background_tasks.add_task(cleanup_images)
    return {"Message": "upload method"}