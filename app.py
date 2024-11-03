from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from ultralytics import YOLO
from flask import flash
import shutil

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
app.config['UPLOAD_FOLDER'] = '/tmp/upload'  #
app.config['PREDICT_FOLDER'] = '/tmp/runs/predict' 

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PREDICT_FOLDER'], exist_ok=True)

# Initialize YOLO model
model = YOLO("Yolov10m_trained.pt")
last_file_name = ""
predict_count = 1

@app.route("/", methods=["GET", "POST"])
def index():
    global last_file_name
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.avi')):
            last_file_name = file.filename
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], last_file_name)
            file.save(upload_path)
            return redirect(url_for("index"))

    # Check if prediction result exists
    predict_path = None
    result_folder = f"result{predict_count - 1}"
    if last_file_name and os.path.exists(os.path.join(app.config['PREDICT_FOLDER'], result_folder, last_file_name)):
        predict_path = f"{app.config['PREDICT_FOLDER']}/{result_folder}/{last_file_name}"
    
    return render_template("index.html", uploaded_file=last_file_name, predicted_file=predict_path, predict_count=predict_count)

@app.route("/predict", methods=["POST"])
def predict():
    global predict_count, last_file_name
    if last_file_name:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], last_file_name)
        output_dir = os.path.join(app.config['PREDICT_FOLDER'], f"result{predict_count}")

        # Run YOLO model prediction
        model.predict(source=input_path, save=True, project=app.config['PREDICT_FOLDER'], name=f"result{predict_count}")
        
        # Update predict_path to the latest prediction result
        predict_path = f"{app.config['PREDICT_FOLDER']}/result{predict_count}/{last_file_name}"
        predict_count += 1  
    
    return redirect(url_for("index", predicted_file=predict_path))

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/runs/predict/<int:n>/<filename>')
def predicted_file(n, filename):
    return send_from_directory(f"{app.config['PREDICT_FOLDER']}/result{n}", filename)

@app.route("/clear_cache", methods=["POST"])
def clear_cache():
    global predict_count, last_file_name
    predict_count = 1
    last_file_name = ""
    
    # Clear all files and subdirectories in the upload and predict folders
    for folder in [app.config['UPLOAD_FOLDER'], app.config['PREDICT_FOLDER']]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    
    flash("Cache cleared successfully!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
