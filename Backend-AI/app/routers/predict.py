from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile
# from .. import modules, utils
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
from typing import Annotated
router = APIRouter(
    prefix='/predict',
    tags=['Prediction']
)
# Test 
def test():
    image_path = Path('app/test_inputs/input_1.png')
    image = Image.open(image_path)
    
    plt.figure(figsize=(5, 5))
    plt.imshow(image)
    plt.axis('off')
    plt.show()
    return image

@router.post('/', status_code = status.HTTP_200_OK)
def post_image(image):
    plt.figure(figsize=(5, 5))
    plt.imshow(image)
    plt.axis('off')
    plt.show()
    return {'message': 'Image uploaded successfully'}

@router.get('/', status_code=status.HTTP_200_OK)
def get_predictions():
    image = test()
    return {"message": "Successfully"}

from fastapi.responses import StreamingResponse
import io
@router.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        # Read file contents
        contents = file.file.read()

        # Save the file to disk
        with open(file.filename, 'wb') as f:
            f.write(contents)

        # Create a Matplotlib figure
        plt.figure(figsize=(5, 5))
        plt.imshow(plt.imread(io.BytesIO(contents)))
        plt.axis('off')

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Return the image as a response
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        return {"message": f"There was an error uploading the file: {str(e)}"}
    finally:
        file.file.close()
# @router.post("/upload")
# def upload(file: UploadFile = File(...)):
#     try:
#         contents = file.file.read()
#         with open(file.filename, 'wb') as f:
#             f.write(contents)
#         plt.figure(figsize=(5, 5))
#         plt.imshow(contents)
#         plt.axis('off')
#         plt.show()
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file.file.close()

#     return {"message": f"Successfully uploaded {file.filename}"}
