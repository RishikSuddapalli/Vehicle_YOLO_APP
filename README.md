![Screenshot 2024-11-18 192236](https://github.com/user-attachments/assets/b009ae27-2f63-4a9c-a05c-bb25dbaae830)
## YOLO Vehicle Detection App - README

This is a web application that utilizes the YOLO object detection model to identify vehicles in images and videos. Users can upload an image or video file, and the app will display the detected vehicles with bounding boxes.

**Features:**

* Supports image and video uploads (JPG, JPEG, AVI, MP4)
* Real-time prediction using the YOLOv9t model
* Displays predicted bounding boxes around detected vehicles
* Option to clear uploaded and predicted files

**Requirements:**

* Python 3.10.15
* Flask framework
* Ultralytics library
* MoviePy library
Reffer to requirement.txt

**Installation:**

1. Clone this repository.
2. Install required dependencies:

   ```bash
   pip install flask ultralytics moviepy
   ```
3. Download a pre-trained YOLO model (e.g., Yolov9t_trained.pt) and place it in the same directory as this README.

**Usage:**

1. Run the application:

   ```bash
   python app.py
   ```
2. Open http://127.0.0.1:5000/ in your web browser.
3. Click on Clear Cache.
![image](https://github.com/user-attachments/assets/3de019e8-aaf5-4ec4-af54-6f82d9cac76e)
4. Click "Choose File" and select an image or video file.
5. Click "Upload Image/Video" to upload the file.
![Screenshot 2024-11-18 192236](https://github.com/user-attachments/assets/3ae568e3-0389-4d33-8d38-636c701383a4)
6. Click "Predict" to run the YOLO model on the uploaded file.
7. The predicted result with bounding boxes will be displayed below the uploaded file.
![Screenshot 2024-11-18 192248](https://github.com/user-attachments/assets/d12c6bc9-6679-4af4-a4d0-5702fb9b7c14)
![Screenshot 2024-11-18 192103](https://github.com/user-attachments/assets/20b4e849-dd95-443e-b773-d6f07ca5389c)

**Clear Cache:**
1. Click the "Clear Cache" button to remove uploaded and predicted files.

**Notes:**

* This application is for demonstration purposes only.
* The accuracy of vehicle detection depends on the quality of the uploaded file and the chosen YOLO model.
* The application can be further customized to display additional information about the detected vehicles.

**Contributing:**

We welcome contributions to this project. Feel free to fork the repository and submit pull requests with your improvements.
