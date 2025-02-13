# Hệ thống tự động phân loại táo dựa trên màu sắc
The topic Automatic fruit sorting conveyor system is carried out with the purpose of automatically sorting fruits on the conveyor belt. With the input of the system being the types of fruits that need to be sorted, the output of the system is fruit boxes with each box containing 1 type of fruit. The system uses a camera from esp32cam to collect images of fruits on the conveyor belt, then the image will be processed and make predictions about the type of fruit, the processing will be handled by the Server, then the results are sent to another kit that the group uses, esp32, to classify the fruits into the corresponding boxes.

## Report: [README DETAIL PDF](./READMEDetail.pdf)
## Slides: [Representation](./Slide.pdf)
## Google Drive (SERVER): [https://drive.google.com/drive](https://drive.google.com/drive/folders/1rNSxV73FJjdwqtn1A5vkjFCKTb-1W1Sy?usp=sharing)
## Use case diagram

![](/images/Usecase-predict-system.png)

![](/images//Usecase-ESP32Client.png)
## Activity diagram
![](/images/Activity-diagram_new.png)
## Server structure
![](/images/SERVER.png)
