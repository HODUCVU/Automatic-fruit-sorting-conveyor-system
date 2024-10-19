# Server
| Function | Description |
|----------|-------------|
| Predict type fruits | Use PyTorch to predict image is apple or orange |
| Deploy   | Use heroku to deploy server, ESP32CAM and ESP32Client can connect to publib server |

:link: :computer: **Server:** https://server-fastapi-2b0eb22f2d67.herokuapp.com/

# Fix latency of server
1. increase computer on server. -> Not ok
2. Using Colab and PyNgrok to deploy serve (temporary) -> Quite Good
- 🖥️ [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Ufo8iX-KTeOn11CYhyvI60IpBDCuAWG3?usp=sharing)

- https://www.youtube.com/watch?v=YYxV_InMGY8&list=LL&index=124&t=1048s
3. Using AWS
- Upload image to AWS.
- FastAPI download Image and predict on local machine (every 1s).
- Upload result on to AWS with file.txt format.

# Fix rate of model
1. Apple Fruit Scab Recognition
- https://debuggercafe.com/apple-fruit-scab-recognition-using-deep-learning-and-pytorch/
2. Fruit Classification
- https://github.com/kanchan1910/Fruit-Classification-using-Feedforward-Neural-Networks-in-PyTorch/blob/master/fruit-classification.ipynb
3. Apple Varieties Classification 
- https://www.researchgate.net/publication/377932029_Apple_Varieties_Classification_Using_Deep_Features_and_Machine_Learning

# Dataset (ALL APPLE VARIETIES DATASET)
1. https://waapple.org/varieties/all/
2. https://universe.roboflow.com/bmstu-o7yzf/apples-of-different-varieties
3. https://www.kaggle.com/code/edwardjross/apple-variety-image-classification/notebook

