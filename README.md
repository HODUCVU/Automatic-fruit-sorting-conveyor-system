# Detect-Object-From-ESP32CAM

<!-- https://www.notion.so/Project-ce108af6dc6c45a6bdb49dc53c04b889?pvs=4 -->
# Table of contents
| Sections | Descriptions | Status | 
|---------|------------|--------|
| [Documentations](#-documentations "Goto Documentations")| Build idea, input, output, tasks and plan for project | <img src="https://github.com/HODUCVU/Detect-Object-From-ESP32CAM/assets/73897430/4209397c-64a3-449a-924b-0729e6c986e9" alt="image" width="50" height="50"> |
| [Object Detection](#-object-detection "Goto Object Detection") | Build model using PyTorch and deploy it onto Web-server using FastAPI| <img src="https://github.com/HODUCVU/Detect-Object-From-ESP32CAM/assets/73897430/832590f3-cf5c-4218-acef-655844302de6" alt="image" width="50" height="50"> |
| [Web-server](#-web-server "Goto Web-server") | Building a web-server to embedded model AI, monitor Camera and control system |  <img src="https://github.com/HODUCVU/Detect-Object-From-ESP32CAM/assets/73897430/832590f3-cf5c-4218-acef-655844302de6" alt="image" width="50" height="50"> |
| [Embedded Artificial Intelligence](#embedded-artificial-intelligence "Goto AI Embedded") | Building a system has hardward and AI, in detail that system can be a robot or similar | <img src="https://github.com/HODUCVU/Detect-Object-From-ESP32CAM/assets/73897430/832590f3-cf5c-4218-acef-655844302de6" alt="image" width="50" height="50">   |
| [Reference papers](#reference-papers "Goto papers") | Research for project |   |
| [Reference code](#reference-code "Goto code") | Implement project |   |
## <img src="https://github.com/HODUCVU/Detect-Object-From-ESP32CAM/assets/73897430/1332b32c-83b9-4bcd-bcc4-627d11a5b5e6" alt="image" width="35" height="35"> Documentations 
[![Notion](https://upload.wikimedia.org/wikipedia/commons/e/e9/Notion-logo.svg)](https://www.notion.so/Project-ce108af6dc6c45a6bdb49dc53c04b889?pvs=4) Project Documentation

## <img src="https://github.com/HODUCVU/Detect-Object-From-ESP32CAM/assets/73897430/800edcc3-721c-444a-9be2-96a8f1e438f1" alt="image" width="35" height="35"> Object Detection 
### Datasets
🔗 **Dataset:** https://www.kaggle.com/datasets/sriramr/apples-bananas-oranges/data?select=original_data_set

<img width="150" alt="Screen Shot 2018-06-08 at 4 59 36 PM" src="https://github.com/user-attachments/assets/c7efef07-d06a-43cd-9c64-1cd8798d8ef8">
<img width="160" alt="Screen Shot 2018-06-12 at 11 50 19 PM" src="https://github.com/user-attachments/assets/48005b38-648f-4aad-b361-e69c807dca9f">

💁 We only use apples and oranges data, so before train model, we need to pre-process dataset:
- First: We need re-oraginal data to apples directory and oranges directory.
- Second: Split data to train and test data. Actually, I want to create two folder (train and test).

🔗 **Pre-processing datasest:**  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1fs8ycZEtu2tMbgSwHToqrfSai0sONN93?usp=sharing) 
### Training models
💁 We have pre-processed data above, now we can train some models with the data.
- In this project, I'm going to use PyTorch to train models.
- I will experiment some models such as ResNet, Efficient, MobileNet...
- See which model is compatible with our project based on criteria such as its accuracy and size.

🔗 **Code**: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1HfSQ2LAKJ0-ZdKWwJImfyQirQ6zOeo3B?usp=sharing) 

✈️ Such as I trained model with ResNet50 module, well, I have some experiment to get a good result like below:

- 📉 This chart is descript for train and test loss/accuracy of model
  
  <img width="500" src="https://github.com/user-attachments/assets/40e5b82b-bdfd-4682-9886-cc9ee407f4e6">
- 🍏🍊 We can make some prediction to see what's going on
  
  <img width="250" src="https://github.com/user-attachments/assets/d1474db1-1817-4769-8e13-b2287f45b668">
  <img width="355" src="https://github.com/user-attachments/assets/270eece8-77de-45b7-b603-3494ef04b28e">

### Evaluating models

| Name model | Accuracy Testing (%) | Accuracy Predict (%) | Time Predict (s) | Size (MB) |
|------------|----------------------|----------------------|------------------|-----------|
| ResNet50   |    98.660714         |      97.001250       |    0.203992      |    89     |
|	ResNet18	 |    97.321429	        |      99.881893	     |    0.178116	    |    42     |
|	MobileNetV2|	  98.660714         |      99.923056	     |    0.170975	    |    8      |

- **⏲️ Shortest predict time:**  MobileNetV2 with 0.17 seconds

- **📁 Smallest size file:** MobileNetV2 with 8 MB

- **📉 Accuracy:** The above three models have similar accuracy rates, but MobileNetV2 is trained with the fewest training iterations (5), while ResNet50 and ResNet18 are trained with 8 iterations.

### Optimizing model

### Conclusion

## <img src="https://github.com/HODUCVU/Detect-Object-From-ESP32CAM/assets/73897430/2e5dbf79-4970-4700-b223-b7c6accf3ecd" alt="image" width="35" height="35"> Web-server
## Embedded Artificial Intelligence
## Reference Papers
| Paper | Link | Quote |
|-------|------|-------------|
| Object Detection using ESP 32 CAM | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4152378 | `Mehendale, Ninad. "Object Detection using ESP 32 CAM." Available at SSRN 4152378 (2022).` |
| Real-Time Reinforcement Learning for Vision-Based Robotics Utilizing Local and Remote Computers | https://arxiv.org/pdf/2210.02317 | `Wang, Yan, Gautham Vasan, and A. Rupam Mahmood. "Real-time reinforcement learning for vision-based robotics utilizing local and remote computers." 2023 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2023.` |
| Flow-guided Semi-supervised Video Object Segmentation | https://arxiv.org/pdf/2301.10492 | `Zhang, Yushan, et al. "Flow-guided semi-supervised video object segmentation." arXiv preprint arXiv:2301.10492 (2023).` |
## Reference Code
| Source | Link | Category |
|--------|------|----------|
| yoursunny/esp32cam | https://github.com/yoursunny/esp32cam | source code (CAM) |
| garythung/trashnet | https://github.com/garythung/trashnet | dataset |

