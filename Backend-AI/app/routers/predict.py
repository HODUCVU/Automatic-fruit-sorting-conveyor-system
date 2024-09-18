
# from fastapi import status, APIRouter, UploadFile
# from pathlib import Path
# from PIL import Image
# from app.utils import modules
# # import threading
# import uuid
# import asyncio

# router = APIRouter(
#     prefix='/predict',
#     tags=['Prediction'],
# )
# # Test 
# model = modules('app/models/mobilenet_v2_model.pth')

# image_dir = []
# IMAGEDIR = "app/test_inputs/"

# # Create a lock for async-safe operations
# image_dir_lock = asyncio.Lock()

# async def clean_memory():
#     # files = [f for f in Path(IMAGEDIR).glob('*') if f.is_file()]
#     async with image_dir_lock:
#         files_to_remove = image_dir[:-5]
#         for file in files_to_remove:
#             file.unlink()  # Removes file
#         del image_dir[:-5]

# @router.get('/', status_code=status.HTTP_200_OK)
# async def get_predictions():
#     if not image_dir:
#         return {"Message": "No image found"}
#     async with image_dir_lock:
#         image = Image.open(image_dir[-1])
#         pred = model.make_predict(image)
#     return {"message": model.classes[pred]}

# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def upload(file: UploadFile | None = None):
#     # with image_dir_lock:
#     if not file:
#         return {"Message": "No upload file sent"}
#     if file.size < 1:
#         return {"Message": "File isn't legal"}
#     if file.size > 1 *1024 * 1024:
#         return {"Message": "File too large"}
#     file.filename = f'{uuid.uuid4()}.jpg'
#     contents = await file.read()
#     image_path = Path(f'{IMAGEDIR}{file.filename}')
#     image_path.parent.mkdir(parents=True, exist_ok=True)
#     with open(image_path, 'wb') as f:
#         f.write(contents)
#     async with image_dir_lock:
#         image_dir.append(image_path)
#         # check len of image_dir, if it over 20 image then delete image
#         if len(image_dir) >= 20:
#             await clean_memory()
#     return {"Uploaded": str(image_path)}

