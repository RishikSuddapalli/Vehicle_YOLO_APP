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
3. Click "Choose File" and select an image or video file.
4. Click "Upload Image/Video" to upload the file.
5. Click "Predict" to run the YOLO model on the uploaded file.
6. The predicted result with bounding boxes will be displayed below the uploaded file.

**Clear Cache:**

1. Click the "Clear Cache" button to remove uploaded and predicted files.

**Notes:**

* This application is for demonstration purposes only.
* The accuracy of vehicle detection depends on the quality of the uploaded file and the chosen YOLO model.
* The application can be further customized to display additional information about the detected vehicles.

**Contributing:**

We welcome contributions to this project. Feel free to fork the repository and submit pull requests with your improvements.
