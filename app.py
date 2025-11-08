import os
import json
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from collections import defaultdict

# Import core logic components
from object_detector import ObjectDetector
from room_identifier import RoomIdentifier
from unique_object_counter import UniqueObjectCounter
from report_generator import ReportGenerator

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output' # This should be the same as in main.py
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize core logic components (can be done once for the app)
detector = ObjectDetector()
room_identifier = RoomIdentifier()
unique_counter = UniqueObjectCounter()
report_generator = ReportGenerator()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

# Add GET route for /upload to render the enhanced upload page
@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files[]')
    room_id_input = request.form.get('room_id', 'Unknown_Room')

    if not files or all(f.filename == '' for f in files):
        return redirect(request.url)

    processed_images = []
    detections_by_room = defaultdict(list)
    
    # Clear previous uploads and outputs to maintain a clean state for each new upload session
    clear_directory(app.config['UPLOAD_FOLDER'])
    clear_directory(os.path.join(app.config['OUTPUT_FOLDER'], "visualizations"))
    clear_directory(app.config['OUTPUT_FOLDER'], exclude_dirs=["visualizations"])

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(filepath)
            
            # Process the uploaded image
            room_id = room_id_input # Using input room ID for now
            # In a more advanced version, you'd classify the room from the image itself

            detections = detector.detect_objects(filepath)
            detections_by_room[room_id].extend(detections)

            # Visualize and save detections for this image
            output_visualization_path = os.path.join(app.config['OUTPUT_FOLDER'], "visualizations", f"detected_{filename}")
            report_generator.visualize_detections(filepath, detections, output_visualization_path)

            processed_images.append({
                "filename": filename,
                "room_id": room_id,
                "detections": detections,
                "visualization_url": url_for('uploaded_file', filename=f"visualizations/detected_{filename}")
            })

    # Generate reports after processing all images
    unique_counts = unique_counter.count_unique_objects(detections_by_room)
    json_report_path = os.path.join(app.config['OUTPUT_FOLDER'], "room_wise_report.json")
    csv_report_path = os.path.join(app.config['OUTPUT_FOLDER'], "room_wise_report.csv")
    report_generator.generate_json_report(unique_counts, json_report_path)
    report_generator.generate_csv_report(unique_counts, csv_report_path)

    # Prepare data for rendering results
    results_data = {
        "processed_images": processed_images,
        "unique_counts": unique_counts,
        "json_report_url": url_for('uploaded_file', filename='room_wise_report.json'),
        "csv_report_url": url_for('uploaded_file', filename='room_wise_report.csv')
    }

    return render_template('results.html', results=results_data)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # This route serves files from the UPLOAD_FOLDER and OUTPUT_FOLDER
    # For simplicity, we are serving directly. In a production environment,
    # you might want more robust file serving.
    upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    output_path = os.path.join(app.root_path, app.config['OUTPUT_FOLDER'])
    
    if os.path.exists(os.path.join(upload_path, filename)):
        return send_from_directory(upload_path, filename)
    elif os.path.exists(os.path.join(output_path, filename)):
        return send_from_directory(output_path, filename)
    elif os.path.exists(os.path.join(output_path, "visualizations", filename)):
        return send_from_directory(os.path.join(output_path, "visualizations"), filename)
    else:
        return "File not found", 404

def clear_directory(directory_path, exclude_dirs=None):
    if os.path.exists(directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if exclude_dirs and item in exclude_dirs:
                continue
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # Recursively clear subdirectories, or remove if not in exclude_dirs
                if item not in exclude_dirs if exclude_dirs else False:
                    import shutil
                    shutil.rmtree(item_path)

if __name__ == '__main__':
    # Ensure necessary directories exist at startup
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "visualizations"), exist_ok=True)
    app.run(debug=True)
