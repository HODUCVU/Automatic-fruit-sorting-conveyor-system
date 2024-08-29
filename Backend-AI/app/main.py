# RUN FASTAPI FROM WSL
# https://smartshock.hashnode.dev/port-forwarding-from-ubuntu-wsl-to-windows-host#heading-step-2-find-the-ip-address-of-ubuntu-wsl

# uvicorn app.main:app --reload   
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# run on http://127.0.0.1:8000/
# python main.py

# check active portL `isof -i:8000`
#  kill port: kill -9 <PID>

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

from routers import predict
app.include_router(predict.router)

@app.get("/")
async def root():
    return {"message": "This is server for pbl5 project"}

if __name__ == "__main__":
    print('SERVER is running...')
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
