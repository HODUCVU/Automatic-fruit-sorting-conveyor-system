# Hệ thống tự động phân loại táo dựa trên màu sắc
The topic Automatic fruit sorting conveyor system is carried out with the purpose of automatically sorting fruits on the conveyor belt. With the input of the system being the types of fruits that need to be sorted, the output of the system is fruit boxes with each box containing 1 type of fruit. The system uses a camera from esp32cam to collect images of fruits on the conveyor belt, then the image will be processed and make predictions about the type of fruit, the processing will be handled by the Server, then the results are sent to another kit that the group uses, esp32, to classify the fruits into the corresponding boxes.
## Sơ đồ kết nối
![image](https://github.com/user-attachments/assets/166e3279-2b31-4e46-b8d8-b90c9cfd3a8b)
## Sản phẩm
![image](https://github.com/user-attachments/assets/a00cdc3c-bdbd-4df2-95fb-60ab202c5072)

## Use case diagram
![](/images/Usecase-predict-system.png)
![](/images//Usecase-ESP32Client.png)
## Activity diagram
![](/images/Activity-diagram_new.png)
## Server structure
![](/images/SERVER.png)
## Một số đoạn code chú ý 
![image](https://github.com/user-attachments/assets/de89be07-b555-43c4-86be-8faffe8740a3)

## Source
- Report: [README DETAIL PDF](./READMEDetail.pdf)
- Slides: [Representation](./Slide.pdf)
- SERVER: [https://drive.google.com/drive](https://drive.google.com/drive/folders/1rNSxV73FJjdwqtn1A5vkjFCKTb-1W1Sy?usp=sharing)

