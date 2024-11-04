from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
from ultralytics import YOLO
import shutil
from moviepy.editor import VideoFileClip

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload')
app.config['PREDICT_FOLDER'] = os.path.join(os.getcwd(), 'runs', 'predict')

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PREDICT_FOLDER'], exist_ok=True)

# Initialize YOLO model
model = YOLO("Yolov9t_trained.pt")
last_file_name = ""
predict_count = 1
predicted_file = None

@app.route("/", methods=["GET", "POST"])
def index():
    global last_file_name, predicted_file
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.lower().endswith(('.jpg', '.jpeg', '.avi', '.mp4')):
            last_file_name = file.filename
            predicted_file = None  # Reset predicted file when a new file is uploaded
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], last_file_name)
            file.save(upload_path)

            # Convert .avi to .mp4 if uploaded
            if last_file_name.lower().endswith('.avi'):
                mp4_path = os.path.splitext(upload_path)[0] + '.mp4'
                try:
                    clip = VideoFileClip(upload_path)
                    clip.write_videofile(mp4_path, codec="libx264")
                    last_file_name = os.path.basename(mp4_path)
                except Exception as e:
                    print(f"Error converting uploaded .avi to .mp4: {e}")

            return redirect(url_for("index"))

    # Set predict_path only if there is a valid predicted file
    predict_path = None
    if predicted_file:
        predict_path = predicted_file
    
    return render_template("index.html", uploaded_file=last_file_name, predicted_file=predict_path, predict_count=predict_count)

@app.route("/predict", methods=["POST"])
def predict():
    global predict_count, last_file_name, predicted_file
    if last_file_name:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], last_file_name)
        output_dir = os.path.join(app.config['PREDICT_FOLDER'], f"result{predict_count}")

        # Run YOLO model prediction
        model.predict(source=input_path, save=True, project=app.config['PREDICT_FOLDER'], name=f"result{predict_count}")

        # Convert the predicted filename for display
        file_root, ext = os.path.splitext(last_file_name)
        if ext.lower() in [".jpg", ".jpeg"]:
            predicted_file = f"{file_root}.jpg"
        elif ext.lower() in [".mp4", ".avi"]:
            predicted_file = f"{file_root}.avi"
            #Convert .avi to .mp4 for browser compatibility
            avi_path = os.path.join(output_dir,f"{file_root}.avi")
            mp4_path = os.path.splitext(avi_path)[0] + '.mp4'
            try:
                clip = VideoFileClip(avi_path)
                clip.write_videofile(mp4_path, codec="libx264")
                predicted_file = os.path.basename(mp4_path)
            except Exception as e:
                print(f"Error converting uploaded .avi to .mp4: {e}")       
        # Update predict_count for the next prediction
        predict_count += 1
    return redirect(url_for("index"))

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/runs/predict/result<int:n>/<filename>')
def predicted_file_route(n, filename):
    return send_from_directory(os.path.join(app.config['PREDICT_FOLDER'], f"result{n}"), filename)

@app.route("/clear_cache", methods=["POST"])
def clear_cache():
    global predict_count, last_file_name, predicted_file
    predict_count = 1
    last_file_name = ""
    predicted_file = None  # Clear the predicted file cache

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
