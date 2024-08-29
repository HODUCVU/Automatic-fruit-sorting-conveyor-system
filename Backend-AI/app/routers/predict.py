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

import uuid
IMAGEDIR = "test_inputs/"
@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file.filename = f'{uuid.uuid4()}.jpg'
    contents = await file.read()
    
    image_dir.append(Path(f'{IMAGEDIR}{file.filename}'))
    image_dir[-1].parent.mkdir(parents=True, exist_ok=True)
    with open(image_dir[-1], 'wb') as f:
        f.write(contents)
    return {"Uploaded": image_dir[-1]}

@router.get('/', status_code=status.HTTP_200_OK)
def get_predictions():
    image = Image.open(image_dir[-1])
    pred = model.make_predict(image)
    return {"message": model.classes[pred]}

# @router.post('/', status_code = status.HTTP_200_OK)
# def post_image(image):
#     # plt.figure(figsize=(5, 5))
#     # plt.imshow(image)
#     # plt.axis('off')
#     # plt.show()
#     return {'message': 'Image uploaded successfully'}



# ===================
#  Stream video
