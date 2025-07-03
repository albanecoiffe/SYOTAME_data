# SYOTAME_data

# Introduction
The SYOTAME project is a project to create an application allowing user to reserve a parking spot, from partner parking.  
This git repository is the data portion of this project. With everything concerning the computer vision model used for this application.  

# Data
For the data used to fine-tuned this model, we used multiple Roboflow dataset as well as our own dataset. For our own dataset we created it via picture of the parking we initialy wanted to use.  

## Roboflow dataset
Initialy we used the the [PKLot dataset](https://public.roboflow.com/object-detection/pklot). With this model we trained a model, but the result were horrible.  
So after seeing that, we choose to use other dataset, also from Roboflow. We ended up using 3 distinct dataset :  
- [parking-space](https://universe.roboflow.com/muhammad-syihab-bdynf/parking-space-ipm1b)  
- [car-space-find](https://universe.roboflow.com/data-a09tr/car-space-find-wozyb)  
- [parking-space](https://universe.roboflow.com/data-a09tr/parking-space-pubnz-ftfle)  

With those dataset, the model train was a bit better, but still not great, so we decided to create our own dataset.

## Personalized dataset
Our personalized dataset, has been created with real picture of the parking we planed to use.  

1. First we took about 100 picture with different light, angles and time of day.  
  
2. Then we had to annotated every pictures by adding bounding boxes. For that step we used [humansignal.com](https://app.humansignal.com/). This website gave us the possiblity to easily mark every picture with bounding boxes. We created 2 labels (empty and occupied), to match the dataset we got from RoboFlow.  
![Label of bounding boxes : empty & occupied](picture_readme/image-1.png)
  
3. After we annoted, by hand, every picture took.
![Parking picture, with bounding boxes around the parking space](picture_readme/image.png)
    Purple for empty and red for occupied.  
      
4. Finaly we split the dataset between train and validation. To do that we used a function from a [git repository](https://raw.githubusercontent.com/EdjeElectronics/Train-and-Deploy-YOLO-Models/refs/heads/main/utils/train_val_split.py). We choos to have 90% of picture in train dataset and 10% of picture in validation dataset.  

After doing all of that with merged this personalizaned dataset with the 3 we found on Roboflow.

# Model
For our model we used google colab to train it. Like that we had access to faster GPU to improve the traning time needed for our model.  
We created an object detection model, fine-tuning a yolo model.  
To have the best possible model we train multiple model using different dataset. In total we train 3 models with 3 different dataset :  
1. With [PKLot dataset](https://public.roboflow.com/object-detection/pklot), using yolov5.  
Result :  
![Picture of parking with 0 bounding boxes, because the model can't detect them, expected : 5 empty, 7 occupied](picture_readme/model1.png)  
2. With 3 Roboflow dataset using yolov8  
Result :  
![Picture of parking with 4 bounding boxes (2 empty, 2 occupied), the model can't detect all of them, expected : 5 empty, 7 occupied](picture_readme/model2.png)  
3. With 3 Roboflow dataset + our personalized dataset, using yolov8  
Result :  
![Picture of parking with 12 bounding boxes (5 empty, 7 occupied), the model detect all of them, expected : 5 empty, 7 occupied](picture_readme/model3.png)  

# Inference
After completing the training of our model, we designed a python file (`get_nb_place.py` or `get_nb_place_img.py`) to use it and write the necessary data in the database. Both of those file take a picture, load the trained model, use the model with the picture a,d write the number of empty place in the databse. The only diferrence, is that the `get_nb_place_img.py` file also display the picture with the bounding boxes.  

We also created file to use the model with a picture (`test_model.py`), a video (`test_video.py`). Both of the files take an input (picture or video), load the trained model, use the model with the input. For the `test_model.py` file, the picture with the bounding boxes is display. For the `test_video.py` file the video is save as `[name_original_video]_detected.mp4` in a demo folder.  

For example, this picture as been thourght the `test_model.py` file :  
![Picture of parking with 12 bounding boxes (5 empty, 7 occupied)](picture_readme/model3.png)  
