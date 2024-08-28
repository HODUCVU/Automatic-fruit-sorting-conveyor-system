# uvicorn app.main:app --reload   
from fastapi import FastAPI

app = FastAPI()

# domain name (CORS)
from fastapi.middleware.cors import CORSMiddleware
# Everyone can access API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from .routers import predict
app.include_router(predict.router)
