# Room-wise Unique Object Detection

## Project Objective
This project aims to build a computer vision system that detects and counts unique objects in rooms from images or videos, ensuring duplicates within the same room are counted only once. Objects detected across different rooms will be counted separately.

## Core Features
1. **Object Detection**: Utilizes YOLOv8 for accurate object detection within various indoor room settings.
2. **Room Identification**: Each input image/frame is tagged with a room ID, either via metadata or a scene classification/segmentation model.
3. **Unique Object Counting**:
    - Within a single room: If the same object appears multiple times, it is counted as one unique instance.
    - Across different rooms: The same object is counted separately for each room it appears in.
4. **Room-wise Report Generation**: Generates structured reports (JSON/CSV) detailing each room and its list of unique objects.
5. **Visualization**: Optionally provides bounding box visualizations on processed images.

## Technical Stack
- **Backend/Model**: Python, YOLOv8 (Ultralytics)
- **Room Classification/Segmentation**: Metadata tags (initial approach)
- **Processing Pipeline**: YOLO for object detection, custom logic for room-wise grouping and deduplication.

## Setup Instructions

### 1. Clone the repository
```bash
# (Assuming you are in the parent directory where Lakshya_SimplyPhi was created)
# cd Lakshya_SimplyPhi
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install ultralytics opencv-python numpy Pillow
```

## Usage

### Command-line Interface (CLI)
To process the sample dataset and generate reports/visualizations via the command-line, run:
```bash
python main.py
```
Reports will be generated in the `Lakshya_SimplyPhi/output` directory.

### Web Interface
To run the web application, execute:
```bash
pip install Flask Werkzeug
python app.py
```
Then, open your web browser and navigate to `http://127.0.0.1:5000/`.

## Sample Test Scenarios
### Scenario 1:
- Input: Photo of a living room with 2 sofas, 3 chairs, 2 TVs
- Expected Output: `Room A = Sofa: 1, Chair: 1, TV: 1`

### Scenario 2:
- Input: Apartment with 2 rooms - Room A (2 TVs), Room B (1 TV)
- Expected Output: `Room A = TV:1, Room B = TV: 1 (Total unique TVs = 2)`

### Scenario 3:
- Input: Studio room with bed + chair + duplicate bed annotation error
- Expected Output: `Room C = Bed: 1, Chair: 1`

## Deliverables
- Working YOLO-based application
- Source code with documentation
- Sample annotated dataset
- Demo video (conceptual)
- Technical report (conceptual)

## Evaluation Criteria
- **Accuracy**: Correct detection and unique counting per room.
- **Robustness**: Handles multiple rooms and duplicate objects correctly.
- **Code Quality**: Clean, modular, well-documented code.
- **Practicality**: Clear pipeline from image to report.
- **Innovation**: Bonus for advanced techniques (scene segmentation, embeddings for uniqueness).
