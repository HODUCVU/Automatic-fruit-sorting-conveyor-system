from fastapi import FastAPI, status, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
#from pyngrok import ngrok
import os
import logging
import nest_asyncio
import uvicorn
import io
logging.basicConfig(level=logging.INFO)

app = FastAPI()

from pydantic import BaseModel

class PredictionRequest(BaseModel):
    prediction: str
    status: str

pred_list = []
@app.get('/predict', status_code=status.HTTP_200_OK)
async def get_predictions():
    try:
      return {'message':pred_list[-1]['prediction']}
    except Exception as e:
      logging.error(f"Error in prediction: {e}")
      raise HTTPException(status_code=500, detail="Error in prediction")
        
@app.post('/upload', status_code=status.HTTP_200_OK)
async def predict(data: PredictionRequest):
    try:
        prediction = data.prediction
        status = data.status
        
        # Log or process the prediction as needed
        logging.info(f"Received prediction: {prediction} with status: {status}")
        
        # You can store it in a list or perform any action you need
        pred_list.append(data.dict())  # Store the prediction in the pred_list
        
        return {"message": "Prediction received successfully", "prediction": prediction, "status": status}
    
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail="Error in prediction")
# Create a public URL using ngrok
#public_url = ngrok.connect(8000)
#print(f"FastAPI is running at: {public_url}")

# # Run the app using Uvicorn directly (without asyncio.run)
uvicorn.run(app, host="0.0.0.0", port=8000)
