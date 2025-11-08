# Room-wise Unique Object Detection System

## Comprehensive Technical Documentation

**Author:** Lakshya Dubey  
**Project Type:** Computer Vision - Object Detection System  
**Technology Stack:** Python, YOLOv8, Flask, OpenCV  
**Date:** November 2025

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Core Components Breakdown](#core-components-breakdown)
4. [Technical Implementation Details](#technical-implementation-details)
5. [Data Flow & Pipeline](#data-flow--pipeline)
6. [Key Design Decisions](#key-design-decisions)
7. [Web Application Architecture](#web-application-architecture)
8. [Interview Preparation Q&A](#interview-preparation-qa)

---

## Project Overview

### Problem Statement

Build a computer vision system that:

- Detects objects in indoor room images
- Identifies which room each object belongs to
- Counts unique objects per room (deduplicates within same room)
- Treats same objects in different rooms as separate entities
- Generates structured reports and visualizations

### Real-World Application

This system can be used for:

- **Real Estate:** Automated property inventory management
- **Insurance:** Asset verification and claims processing
- **Interior Design:** Room content analysis
- **Property Management:** Furniture and equipment tracking

### Core Objectives Met

✅ Accurate object detection using state-of-the-art YOLOv8  
✅ Room-based object organization  
✅ Intelligent deduplication within rooms  
✅ Multiple interface options (CLI & Web)  
✅ Comprehensive reporting (JSON/CSV)  
✅ Visual feedback with bounding boxes

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
│  ┌──────────────────────┐    ┌─────────────────────────┐   │
│  │   Web Interface      │    │   CLI Interface         │   │
│  │   (Flask App)        │    │   (main.py)             │   │
│  └──────────────────────┘    └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    CORE PROCESSING LAYER                     │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ ObjectDetector│  │RoomIdentifier│  │UniqueObject     │  │
│  │   (YOLOv8)    │  │  (Metadata)  │  │Counter          │  │
│  └───────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      OUTPUT GENERATION                       │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ ReportGenerator│  │ Visualization│  │  JSON/CSV       │  │
│  │  (Reports)     │  │  (Bounding   │  │  Files          │  │
│  │                │  │   Boxes)     │  │                 │  │
│  └───────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack Justification

**1. YOLOv8 (You Only Look Once v8)**

- **Why chosen:** State-of-the-art real-time object detection
- **Advantages:**
  - High accuracy with fast inference speed
  - Pre-trained on COCO dataset (80+ object classes)
  - Excellent for indoor object detection (furniture, electronics)
  - Easy integration via Ultralytics library
  - Supports multiple model sizes (nano, small, medium, large)
- **Model Used:** `yolov8n.pt` (nano version)
  - Fastest inference time
  - Good balance between speed and accuracy
  - Suitable for web deployment

**2. Flask Framework**

- **Why chosen:** Lightweight Python web framework
- **Advantages:**
  - Easy to learn and implement
  - Perfect for ML model deployment
  - Built-in development server
  - Flexible routing and templating
  - Small overhead

**3. OpenCV (cv2)**

- **Why chosen:** Industry-standard computer vision library
- **Use cases in project:**
  - Image loading and processing
  - Drawing bounding boxes
  - Image manipulation and saving
  - Format conversions

**4. Python Standard Libraries**

- **collections.defaultdict:** Efficient grouping of detections by room
- **json & csv:** Standard report generation formats
- **os:** File system operations and path management

---

## Core Components Breakdown

### 1. object_detector.py - The Vision Engine

```python
class ObjectDetector:
    def __init__(self, model_name='yolov8n.pt'):
        self.model = YOLO(model_name)
        self.class_names = self.model.names
```

**Purpose:** Handles all object detection using YOLOv8

**Key Methods:**

#### a) `detect_objects(image_path)`

**What it does:**

- Loads the image from given path
- Runs YOLOv8 inference
- Extracts bounding boxes, confidence scores, and class labels
- Returns structured detection data

**Technical Flow:**

```
Image Input → YOLOv8 Model → Raw Results → Parse Boxes →
Extract Coordinates → Map Class IDs to Names → Return Detections
```

**Data Structure Returned:**

```python
[
    {
        "box": [x1, y1, x2, y2],      # Bounding box coordinates
        "confidence": 0.92,             # Detection confidence (0-1)
        "class_name": "chair"           # Object class name
    },
    ...
]
```

**Why this structure:**

- Box coordinates enable visualization
- Confidence allows filtering low-quality detections
- Class name is human-readable for reports

#### b) `draw_boxes(image_path, detections, output_path)`

**What it does:**

- Draws green bounding boxes on image
- Adds text labels with class name and confidence
- Saves annotated image or displays it

**Technical Details:**

- Uses OpenCV's `cv2.rectangle()` for boxes
- Uses `cv2.putText()` for labels
- Color: Green (0, 255, 0) for visibility
- Font: HERSHEY_SIMPLEX for clarity

**Why separate from detection:**

- Separation of concerns principle
- Detection can be used without visualization
- Allows different visualization styles

---

### 2. room_identifier.py - Room Association

```python
class RoomIdentifier:
    def get_room_id(self, image_metadata):
        return image_metadata.get('room_id')
```

**Purpose:** Associates images with room IDs

**Current Implementation:**

- **Metadata-based:** Reads room ID from metadata.json
- **Simple and reliable:** No ML overhead
- **Production-ready:** For controlled environments

**Design Choice:**

- Started with simple metadata approach
- Allows focus on core object detection
- Easily extendable to ML-based room classification

**Future Enhancement Placeholder:**

```python
# Planned: Scene classification using CNN
def classify_room_from_image(self, image_path):
    # Would use models like ResNet or Places365
    # To automatically detect room types
    pass
```

**Why metadata approach for now:**

1. **Simplicity:** No additional model training needed
2. **Reliability:** 100% accuracy if metadata is correct
3. **Speed:** No inference overhead
4. **Flexibility:** Users can define custom room IDs

---

### 3. unique_object_counter.py - Deduplication Logic

```python
class UniqueObjectCounter:
    def count_unique_objects(self, detections_by_room):
        for room_id, detections in detections_by_room.items():
            unique_objects_in_room = set()
            for det in detections:
                unique_objects_in_room.add(det['class_name'])
```

**Purpose:** Counts unique objects per room (core business logic)

**Algorithm Explanation:**

**Step-by-Step Process:**

1. **Input:** Dictionary with room IDs as keys, detection lists as values
2. **For each room:**
   - Create empty set (automatically handles duplicates)
   - Add each detected object's class name to set
   - Sets naturally deduplicate (same name added multiple times = stored once)
3. **Output:** Dictionary with room IDs and unique object counts

**Example Scenario:**

```python
Input:
{
    "Living Room": [
        {"class_name": "chair"},
        {"class_name": "chair"},  # Duplicate
        {"class_name": "chair"},  # Duplicate
        {"class_name": "tv"},
        {"class_name": "sofa"}
    ]
}

Processing:
- unique_objects_in_room = set()
- Add "chair" → set becomes {"chair"}
- Add "chair" → set stays {"chair"} (duplicate ignored)
- Add "chair" → set stays {"chair"} (duplicate ignored)
- Add "tv" → set becomes {"chair", "tv"}
- Add "sofa" → set becomes {"chair", "tv", "sofa"}

Output:
{
    "Living Room": {
        "chair": 1,
        "tv": 1,
        "sofa": 1
    }
}
```

**Why Python Sets:**

- **Automatic deduplication:** No manual checking needed
- **O(1) add operation:** Constant time complexity
- **Memory efficient:** Stores unique values only
- **Built-in:** No external libraries needed

**Important Design Decision:**

- Count is always 1 per unique object type
- Focuses on "presence" not "quantity"
- Meets requirement: "duplicates in same room count as one"

---

### 4. report_generator.py - Output Generation

```python
class ReportGenerator:
    def generate_json_report(self, unique_counts_by_room, output_filepath)
    def generate_csv_report(self, unique_counts_by_room, output_filepath)
    def visualize_detections(self, image_path, detections, output_path)
```

**Purpose:** Generates multiple output formats

#### a) JSON Report Generation

**Why JSON:**

- **Machine-readable:** Easy to parse programmatically
- **Structured:** Hierarchical data representation
- **Standard:** Universal format for APIs
- **Compact:** Efficient storage

**Output Format:**

```json
{
  "Living Room A": {
    "chair": 1,
    "tv": 1,
    "sofa": 1
  },
  "Bedroom B": {
    "bed": 1,
    "lamp": 1
  }
}
```

#### b) CSV Report Generation

**Why CSV:**

- **Human-readable:** Open in Excel/Sheets
- **Simple:** Easy to understand
- **Portable:** Works everywhere
- **Analyzable:** Easy data analysis

**Output Format:**

```csv
Room ID,Object,Count
Living Room A,chair,1
Living Room A,tv,1
Living Room A,sofa,1
Bedroom B,bed,1
Bedroom B,lamp,1
```

#### c) Visualization Method

**Technical Implementation:**

- Reads original image using OpenCV
- Iterates through all detections
- Draws rectangle: `cv2.rectangle(img, (x1,y1), (x2,y2), color, thickness)`
- Adds text label: `cv2.putText(img, label, position, font, size, color, thickness)`
- Saves to output directory

**Color Scheme:**

- Green (0, 255, 0): Standard for "detected" objects
- Visible on most backgrounds
- Professional appearance

---

## Technical Implementation Details

### Main Pipeline (main.py) - CLI Execution

**Complete Workflow:**

```python
def main(dataset_path, output_dir):
    # 1. INITIALIZATION PHASE
    detector = ObjectDetector()           # Load YOLOv8 model
    room_identifier = RoomIdentifier()    # Initialize room ID handler
    unique_counter = UniqueObjectCounter() # Initialize counter
    report_generator = ReportGenerator()   # Initialize report generator

    # 2. SETUP PHASE
    os.makedirs(output_dir, exist_ok=True)           # Create output directory
    os.makedirs(output_dir + "/visualizations")     # Create viz directory

    # 3. METADATA LOADING
    with open(metadata_path) as f:
        metadata = json.load(f)  # Load room assignments

    # 4. DATA COLLECTION PHASE
    all_detections_by_room = defaultdict(list)

    for image_name, img_metadata in metadata.items():
        # Get image path
        image_path = dataset_path + "/" + image_name

        # Extract room ID from metadata
        room_id = room_identifier.get_room_id(img_metadata)

        # Detect objects in image
        detections = detector.detect_objects(image_path)

        # Group detections by room
        all_detections_by_room[room_id].extend(detections)

        # Generate visualization
        output_viz_path = output_dir + "/visualizations/detected_" + image_name
        report_generator.visualize_detections(image_path, detections, output_viz_path)

    # 5. PROCESSING PHASE
    unique_counts = unique_counter.count_unique_objects(all_detections_by_room)

    # 6. REPORT GENERATION PHASE
    report_generator.generate_json_report(unique_counts, output_dir + "/report.json")
    report_generator.generate_csv_report(unique_counts, output_dir + "/report.csv")
```

**Why this order:**

1. Initialize all components first (fail fast if missing dependencies)
2. Setup directories before writing files
3. Load metadata once (efficiency)
4. Process all images before counting (complete dataset)
5. Generate all reports at end (consistency)

---

### Web Application (app.py) - Flask Implementation

**Architecture Overview:**

```
Client Browser ←→ Flask Server ←→ Core Logic Modules ←→ File System
     (HTML)         (Routes)      (Detection/Counting)     (Storage)
```

#### Key Flask Configurations

```python
UPLOAD_FOLDER = 'uploads'      # User-uploaded images
OUTPUT_FOLDER = 'output'       # Generated reports/visualizations
MAX_CONTENT_LENGTH = 16 MB     # Upload size limit
ALLOWED_EXTENSIONS = {png, jpg, jpeg, gif}
```

**Why these settings:**

- **16MB limit:** Prevents server overload, reasonable for photos
- **Specific extensions:** Security (no executable files)
- **Separate folders:** Organization and security

#### Route 1: Homepage (`/`)

```python
@app.route('/')
def index():
    return render_template('index.html')
```

**Purpose:** Landing page with project description and upload form

**What it shows:**

- Project title and description
- Simple upload form
- How it works section
- Instructions for use

#### Route 2: Upload Page (`/upload` GET)

```python
@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')
```

**Purpose:** Enhanced upload interface

**Features:**

- Drag-and-drop file upload
- File preview before processing
- Progress bar during processing
- Multiple file selection
- Room ID input field

#### Route 3: Process Upload (`/upload` POST)

```python
@app.route('/upload', methods=['POST'])
def upload_file():
    # 1. FILE VALIDATION
    if 'files[]' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files[]')
    room_id = request.form.get('room_id', 'Unknown_Room')

    # 2. DIRECTORY CLEANUP
    clear_directory(UPLOAD_FOLDER)
    clear_directory(OUTPUT_FOLDER)

    # 3. FILE PROCESSING LOOP
    processed_images = []
    detections_by_room = defaultdict(list)

    for file in files:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = UPLOAD_FOLDER + "/" + filename
        file.save(filepath)

        # Detect objects
        detections = detector.detect_objects(filepath)
        detections_by_room[room_id].extend(detections)

        # Create visualization
        viz_path = OUTPUT_FOLDER + "/visualizations/detected_" + filename
        report_generator.visualize_detections(filepath, detections, viz_path)

        # Store for display
        processed_images.append({
            "filename": filename,
            "room_id": room_id,
            "detections": detections,
            "visualization_url": url_for('uploaded_file', ...)
        })

    # 4. GENERATE REPORTS
    unique_counts = unique_counter.count_unique_objects(detections_by_room)
    report_generator.generate_json_report(unique_counts, ...)
    report_generator.generate_csv_report(unique_counts, ...)

    # 5. RENDER RESULTS
    return render_template('results.html', results=results_data)
```

**Critical Security Features:**

1. **secure_filename():**

   - Removes path traversal attempts
   - Sanitizes special characters
   - Prevents directory escaping

2. **File extension validation:**

   ```python
   def allowed_file(filename):
       return '.' in filename and \
              filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   ```

   - Prevents executable uploads
   - Case-insensitive check
   - Requires extension

3. **Directory cleanup:**
   - Prevents disk space issues
   - Removes old sessions
   - Fresh state for each upload

**Why cleanup between uploads:**

- Prevents confusion between sessions
- Manages disk space
- Ensures report accuracy (only current session data)

#### Route 4: File Serving (`/uploads/<path:filename>`)

```python
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # Check in upload folder
    if exists(UPLOAD_FOLDER + filename):
        return send_from_directory(UPLOAD_FOLDER, filename)
    # Check in output folder
    elif exists(OUTPUT_FOLDER + filename):
        return send_from_directory(OUTPUT_FOLDER, filename)
    # Check in visualizations subfolder
    elif exists(OUTPUT_FOLDER + "/visualizations/" + filename):
        return send_from_directory(OUTPUT_FOLDER + "/visualizations", filename)
    else:
        return "File not found", 404
```

**Why this approach:**

- Single endpoint for all file serving
- Checks multiple locations
- Proper 404 handling
- Secure (no directory traversal)

---

## Data Flow & Pipeline

### Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: INPUT                                                    │
│ User uploads images + provides Room ID                           │
│ ↓                                                                │
│ Files saved to: uploads/image1.jpg, uploads/image2.jpg          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: OBJECT DETECTION                                         │
│ For each image:                                                  │
│   image → YOLOv8 Model → Bounding Boxes + Class Names          │
│ ↓                                                                │
│ Output: [                                                        │
│   {"box": [10,20,100,150], "class_name": "chair", "conf": 0.9},│
│   {"box": [200,50,300,200], "class_name": "tv", "conf": 0.85}  │
│ ]                                                                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: ROOM ASSOCIATION                                         │
│ Group detections by room:                                        │
│ {                                                                │
│   "Living Room": [detection1, detection2, detection3],          │
│   "Bedroom": [detection4, detection5]                           │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: UNIQUE COUNTING                                          │
│ For "Living Room" with [chair, chair, tv, sofa]:                │
│   → set("chair", "tv", "sofa")  # Automatic deduplication       │
│   → {"chair": 1, "tv": 1, "sofa": 1}                           │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: REPORT GENERATION                                        │
│ ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐│
│ │  JSON Report │  │  CSV Report  │  │  Visualized Images     ││
│ │  (Machine)   │  │  (Human)     │  │  (Bounding Boxes)      ││
│ └──────────────┘  └──────────────┘  └────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: RESULTS DISPLAY                                          │
│ Web page shows:                                                  │
│ - Visualized images with boxes                                   │
│ - Unique object counts per room                                  │
│ - Download links for reports                                     │
└─────────────────────────────────────────────────────────────────┘
```

### State Management

**Session Cleanup Strategy:**

```python
def clear_directory(directory_path, exclude_dirs=None):
    # Recursively removes all files and subdirectories
    # Except those in exclude_dirs list
    # Ensures clean state for new upload session
```

**Why important:**

- Prevents mixing data from different sessions
- Manages disk space efficiently
- Avoids stale data in reports

---

## Key Design Decisions

### 1. Modular Architecture

**Decision:** Separate files for each major component

**Reasoning:**

- **Maintainability:** Easy to update individual components
- **Testability:** Each module can be tested independently
- **Reusability:** Components can be used in other projects
- **Clarity:** Clear separation of concerns

**Modules:**

```
object_detector.py      → Detection logic
room_identifier.py      → Room association
unique_object_counter.py → Deduplication
report_generator.py     → Output generation
app.py                  → Web interface
main.py                 → CLI interface
```

### 2. YOLOv8 Model Choice

**Decision:** Use YOLOv8n (nano model)

**Why not larger models:**
| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| YOLOv8n | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | **Our choice** - Fast web deployment |
| YOLOv8s | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Balanced |
| YOLOv8m | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | High accuracy needed |
| YOLOv8l | ⚡⚡ | ⭐⭐⭐⭐⭐⭐ | Research |
| YOLOv8x | ⚡ | ⭐⭐⭐⭐⭐⭐⭐ | Maximum accuracy |

**Our reasoning:**

- Indoor furniture detection doesn't need highest accuracy
- Fast response time important for web application
- Smaller model size (easier deployment)
- Good enough for 80+ COCO classes

### 3. Set-based Deduplication

**Decision:** Use Python sets for uniqueness

**Alternatives considered:**

**Option A: Manual tracking (Rejected)**

```python
# Inefficient approach
unique_objects = []
for detection in detections:
    if detection['class_name'] not in unique_objects:
        unique_objects.append(detection['class_name'])
```

**Why rejected:** O(n) lookup time, more code

**Option B: Dictionary counting (Rejected)**

```python
# Overcomplicated approach
counts = {}
for detection in detections:
    if detection['class_name'] in counts:
        counts[detection['class_name']] += 1
    else:
        counts[detection['class_name']] = 1
```

**Why rejected:** Need uniqueness, not quantities

**Option C: Sets (Chosen) ✓**

```python
unique_objects = set()
for detection in detections:
    unique_objects.add(detection['class_name'])
```

**Why chosen:**

- O(1) lookup and insert
- Automatic deduplication
- Clean, readable code
- Built-in Python feature

### 4. Dual Interface (CLI + Web)

**Decision:** Provide both command-line and web interfaces

**Reasoning:**

**CLI (main.py):**

- **Batch processing:** Process entire datasets
- **Automation:** Can be scripted
- **Development:** Quick testing during development
- **Server environments:** No GUI needed

**Web (app.py):**

- **User-friendly:** Non-technical users
- **Visual feedback:** See results immediately
- **Interactive:** Upload and see results
- **Deployment:** Accessible from anywhere

**Code reuse:**

- Both interfaces use same core modules
- DRY principle (Don't Repeat Yourself)
- Single source of truth for logic

### 5. Metadata vs ML for Room Identification

**Decision:** Start with metadata-based approach

**Comparison:**

| Approach                  | Pros                                                           | Cons                                                     | When to Use                                   |
| ------------------------- | -------------------------------------------------------------- | -------------------------------------------------------- | --------------------------------------------- |
| **Metadata** (Our choice) | ✓ 100% accurate<br>✓ No training<br>✓ Fast<br>✓ No ML overhead | ✗ Manual tagging<br>✗ Not automatic                      | Controlled environments,<br>Existing metadata |
| **ML Classification**     | ✓ Automatic<br>✓ No manual work<br>✓ Scalable                  | ✗ Training needed<br>✗ May have errors<br>✗ More complex | Wild data,<br>No metadata available           |

**Future upgrade path:**

- Add CNN-based scene classification (ResNet/Places365)
- Fall back to metadata if available
- Best of both worlds

### 6. Report Format Choices

**Decision:** Provide both JSON and CSV

**JSON for:**

- API integration
- Machine processing
- Hierarchical structure
- Further analysis

**CSV for:**

- Human review
- Excel/Sheets analysis
- Stakeholder reports
- Non-technical users

**Why both:**

- Different use cases
- No significant overhead
- Increases utility

### 7. File Upload Security

**Security measures implemented:**

1. **Filename sanitization:**

   ```python
   filename = secure_filename(file.filename)
   ```

   - Removes `../` and other path traversal
   - Strips special characters
   - Prevents directory escaping

2. **Extension validation:**

   ```python
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
   ```

   - Whitelist approach (only allow specific)
   - Prevents executable uploads
   - Case-insensitive check

3. **Size limits:**

   ```python
   MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
   ```

   - Prevents DoS attacks
   - Server resource protection
   - Reasonable for photos

4. **Directory isolation:**
   - Uploads go to dedicated folder
   - No mixing with application code
   - Easy to secure/backup

---

## Web Application Architecture

### Frontend Design

**HTML Templates Structure:**

```
templates/
├── index.html      → Landing page with simple form
├── upload.html     → Enhanced upload page with preview
└── results.html    → Results display with visualizations
```

**CSS Architecture:**

```
static/
└── style.css       → Modern monochromatic design system
```

**Design System Features:**

- **CSS Custom Properties:** Consistent colors/spacing
- **Dark Theme:** Modern, professional look
- **Responsive:** Works on mobile/desktop
- **Animations:** Smooth transitions and feedback
- **Accessibility:** Good contrast ratios

**Key Design Elements:**

```css
:root {
  --bg-primary: #0a0a0a; /* Main background */
  --text-primary: #ffffff; /* Main text */
  --accent: #ffffff; /* Interactive elements */
  --radius-md: 12px; /* Border radius */
  --transition-base: 300ms; /* Animation speed */
}
```

**Why this design:**

- Professional appearance for internship presentation
- Modern aesthetic (shows attention to UI/UX)
- Dark theme reduces eye strain
- Smooth animations show polish

### Backend Route Design

**Flask Application Structure:**

```
/                    → Home page (GET)
/upload              → Upload interface (GET)
/upload              → Process upload (POST)
/uploads/<filename>  → Serve files (GET)
```

**RESTful principles applied:**

- GET for retrieval
- POST for data submission
- Appropriate status codes
- Clear URL structure

---

## Interview Preparation Q&A

### Technical Questions & Answers

#### Q1: "Why did you choose YOLOv8 over other object detection models?"

**Your Answer:**
"I chose YOLOv8 for several technical reasons:

1. **State-of-the-art accuracy:** YOLOv8 is the latest in the YOLO series, offering improved accuracy over previous versions while maintaining real-time performance.

2. **Pre-trained on COCO dataset:** The model comes pre-trained on 80+ object classes, which includes all common indoor furniture and electronics like chairs, sofas, TVs, beds, etc. This eliminates the need for custom training.

3. **Easy integration:** The Ultralytics library provides a clean Python API that made integration straightforward.

4. **Model size options:** YOLOv8 offers multiple model sizes (nano to extra-large). I chose the nano version (yolov8n.pt) for fast inference, which is crucial for a web application where users expect quick responses.

5. **Compared to alternatives:**
   - **R-CNN family:** More accurate but much slower, not suitable for real-time web applications
   - **SSD:** Good speed but lower accuracy than YOLO
   - **EfficientDet:** Good balance but more complex to implement
   - **YOLOv8:** Best balance of speed, accuracy, and ease of use for this use case"

---

#### Q2: "How does your deduplication algorithm work?"

**Your Answer:**
"The deduplication is handled in the `UniqueObjectCounter` class using Python sets. Here's the algorithm:

1. **Input structure:** I receive a dictionary where keys are room IDs and values are lists of detections.

2. **For each room:** I create an empty set. Sets in Python automatically handle uniqueness - if you add the same element multiple times, it's stored only once.

3. **Process detections:** I iterate through all detections in a room and add each object's class name to the set. For example, if I detect 3 chairs, I add 'chair' three times, but the set only stores it once.

4. **Count generation:** I then convert this set into a dictionary with counts of 1 for each unique object.

**Example:**

```python
detections = [
    {'class_name': 'chair'},
    {'class_name': 'chair'},  # Duplicate
    {'class_name': 'tv'}
]

unique_objects = set()
for det in detections:
    unique_objects.add(det['class_name'])
# Result: unique_objects = {'chair', 'tv'}

output = {obj: 1 for obj in unique_objects}
# Result: {'chair': 1, 'tv': 1}
```

**Complexity:** This approach is O(n) time where n is the number of detections, and uses O(k) space where k is the number of unique objects. The set operations (add) are O(1) average case."

---

#### Q3: "How do you handle the same object appearing in different rooms?"

**Your Answer:**
"This is a key requirement of the project. My solution handles it through the data structure organization:

1. **Grouping first:** Before any deduplication happens, I group all detections by their room ID using a defaultdict. This creates separate lists for each room.

2. **Independent processing:** Each room's detections are processed independently. The deduplication only happens within a single room's detection list.

3. **Example scenario:**

   - Room A has: [tv, tv, chair] → Output: {tv: 1, chair: 1}
   - Room B has: [tv, bed] → Output: {tv: 1, bed: 1}

   The same 'tv' in both rooms is counted separately because they're in different dictionary keys.

4. **Final output:**
   ```python
   {
       'Room A': {'tv': 1, 'chair': 1},
       'Room B': {'tv': 1, 'bed': 1}
   }
   ```

**Key insight:** By organizing the data structure with rooms as the top-level keys, the deduplication naturally happens at the correct scope (per-room), and objects in different rooms are automatically kept separate."

---

#### Q4: "What security measures did you implement for file uploads?"

**Your Answer:**
"I implemented multiple layers of security for file uploads:

1. **Filename sanitization:** I use Flask's `secure_filename()` function which:

   - Removes path traversal attempts (../)
   - Strips special characters
   - Prevents directory escaping attacks

2. **Extension validation:**

   - Whitelist approach: only allow .png, .jpg, .jpeg, .gif
   - Case-insensitive checking
   - Prevents upload of executable files (.exe, .sh, .php)

3. **File size limits:**

   - Set maximum upload size to 16MB
   - Prevents DoS attacks through large files
   - Configured at Flask app level: `MAX_CONTENT_LENGTH`

4. **Directory isolation:**

   - Uploads saved to dedicated 'uploads' folder
   - Separate from application code
   - Easy to secure with proper permissions

5. **File serving security:**
   - Serve files using Flask's `send_from_directory()`
   - Prevents directory traversal in file serving
   - Returns proper 404 for non-existent files

These measures protect against common web vulnerabilities like path traversal, arbitrary code execution, and DoS attacks."

---

#### Q5: "How would you scale this system for production?"

**Your Answer:**
"For production deployment, I would implement several improvements:

**1. Backend Scaling:**

- **Async processing:** Use Celery with Redis for asynchronous task queue
  - User uploads → immediate response → processing happens in background
  - Prevents timeout issues with multiple/large images
- **Database integration:** Currently file-based, would add PostgreSQL to:

  - Store detection results
  - Track user sessions
  - Enable querying and analytics

- **Caching:** Implement Redis caching for:
  - Previously processed images (hash-based)
  - Model outputs
  - Reduces redundant computation

**2. Model Optimization:**

- **Model quantization:** Convert YOLOv8 to INT8 for faster inference
- **Batch processing:** Process multiple images in single model call
- **GPU utilization:** Deploy with CUDA support for 10x speed improvement

**3. Infrastructure:**

- **Containerization:** Docker containers for consistent deployment
- **Load balancing:** Nginx reverse proxy with multiple Flask workers
- **Auto-scaling:** Kubernetes for automatic scaling based on load
- **CDN:** CloudFlare or AWS CloudFront for static assets

**4. Storage:**

- **Object storage:** Move from local files to S3/Azure Blob
- **Temporary storage:** Auto-delete old uploads after 24 hours
- **Database:** PostgreSQL with proper indexing

**5. Monitoring:**

- **Logging:** Structured logging with ELK stack
- **Metrics:** Prometheus for performance monitoring
- **Alerting:** Alert on high error rates or slow responses

**6. Security Enhancements:**

- **Authentication:** Add user login system
- **Rate limiting:** Prevent abuse (e.g., 10 requests per minute)
- **HTTPS:** SSL certificates for encrypted communication
- **API keys:** For programmatic access

**7. API Development:**

- **RESTful API:** Separate from web interface
- **Documentation:** OpenAPI/Swagger docs
- **Versioning:** API version management

**Cost-effective approach:**

- Start with single AWS EC2 instance
- Add load balancer when traffic increases
- Scale horizontally by adding more instances
- Use managed services (RDS, S3) to reduce ops overhead"

---

#### Q6: "Explain your project's pipeline from start to finish."

**Your Answer:**
"The complete pipeline has 6 main stages:

**Stage 1: Input Reception**

- Web: User uploads images via Flask form
- CLI: Script reads from sample_dataset directory
- Room ID is provided (metadata or user input)

**Stage 2: Object Detection**

- Each image is fed to YOLOv8 model
- Model returns: bounding boxes, confidence scores, class IDs
- I parse this into structured format:
  ```python
  {
    'box': [x1, y1, x2, y2],
    'confidence': 0.92,
    'class_name': 'chair'
  }
  ```

**Stage 3: Room Association**

- Detections are grouped by room ID
- Uses defaultdict for automatic list creation
- Structure: `{room_id: [detection1, detection2, ...]}`

**Stage 4: Deduplication**

- For each room separately:
  - Extract all class names
  - Add to a set (automatic deduplication)
  - Create count dictionary with all values = 1
- Result: `{room_id: {object: 1, object2: 1}}`

**Stage 5: Visualization**

- Original images are loaded with OpenCV
- For each detection:
  - Draw green rectangle (bounding box)
  - Add text label (class name + confidence)
- Save to output/visualizations/

**Stage 6: Report Generation**

- JSON report: Machine-readable structure
- CSV report: Human-readable tabular format
- Both contain same unique counts data
- Saved to output directory

**Stage 7: Results Display**

- Web: Renders results.html with:
  - Visualized images
  - Unique counts table
  - Download links for reports
- CLI: Prints to console and saves files

**Data flow:**

```
Images → YOLO → Detections → Group by Room → Deduplicate →
→ Generate Reports → Visualize → Display Results
```

**Key design principle:** Each stage is independent and testable. If one stage fails, I can debug it in isolation."

---

#### Q7: "What challenges did you face and how did you solve them?"

**Your Answer:**
"I encountered several interesting challenges:

**Challenge 1: Handling Multiple File Uploads**

- **Problem:** Flask's request.files.get() only gets single file
- **Solution:** Used request.files.getlist('files[]') with array notation in HTML
- **Learning:** Understanding Flask's multipart form data handling

**Challenge 2: Deduplication Logic**

- **Problem:** Initially overcomplicated with manual tracking
- **Solution:** Realized Python sets naturally handle this
- **Learning:** Sometimes the simple solution is the best

**Challenge 3: File Serving**

- **Problem:** Needed to serve files from multiple directories (uploads, output, visualizations)
- **Solution:** Created single route that checks all locations in order
- **Learning:** DRY principle - one route with smart logic better than multiple routes

**Challenge 4: Session Management**

- **Problem:** Multiple users would mix their results
- **Solution:** Implemented directory cleanup before each new upload session
- **Future improvement:** Would use session IDs with database

**Challenge 5: YOLOv8 Integration**

- **Problem:** Understanding the output format from YOLO
- **Solution:** Printed and analyzed the results object structure
- **Learning:** RTFM (Read The Fine Manual) - Ultralytics docs were helpful

**Challenge 6: Visualization Quality**

- **Problem:** Bounding boxes overlapping with text labels
- **Solution:** Positioned text above box (y1 - 10)
- **Learning:** Small adjustments make big UX difference

**Challenge 7: Web Interface Design**

- **Problem:** Making it look professional without heavy framework
- **Solution:** Used CSS custom properties for design system
- **Learning:** Modern CSS is powerful enough without frameworks"

---

#### Q8: "How do you test your code?"

**Your Answer:**
"I implemented testing at multiple levels:

**1. Unit Testing Approach:**
Each module has a `if __name__ == '__main__':` block for standalone testing:

```python
# object_detector.py
if __name__ == '__main__':
    detector = ObjectDetector()
    detections = detector.detect_objects('sample.jpg')
    print(detections)  # Verify output format
```

**2. Test Scenarios:**
I created three specific test scenarios based on requirements:

- **Scenario 1:** Living room with duplicates

  - Input: 2 sofas, 3 chairs, 2 TVs
  - Expected: sofa:1, chair:1, tv:1
  - Tests: Basic deduplication

- **Scenario 2:** Multiple rooms

  - Input: Room A (2 TVs), Room B (1 TV)
  - Expected: Room A {tv:1}, Room B {tv:1}
  - Tests: Room separation

- **Scenario 3:** Duplicate error
  - Input: Bed detected twice in same room
  - Expected: bed:1
  - Tests: Error tolerance

**3. Integration Testing:**

- Tested complete pipeline with sample dataset
- Verified JSON and CSV outputs manually
- Checked visualizations for correct bounding boxes

**4. Web Application Testing:**

- Tested file upload with various file types
- Tried edge cases: no file, wrong extension, multiple files
- Verified error handling

**5. What I would add for production:**

```python
import pytest

def test_unique_counting():
    counter = UniqueObjectCounter()
    detections = {
        'Room A': [
            {'class_name': 'chair'},
            {'class_name': 'chair'},
        ]
    }
    result = counter.count_unique_objects(detections)
    assert result == {'Room A': {'chair': 1}}

def test_file_validation():
    assert allowed_file('image.jpg') == True
    assert allowed_file('script.exe') == False
```

**6. Manual Testing Checklist:**

- ✓ Upload single image
- ✓ Upload multiple images
- ✓ Same room, multiple images
- ✓ Different rooms
- ✓ Invalid file type
- ✓ Large file (>16MB)
- ✓ Empty upload
- ✓ Special characters in filename"

---

### Behavioral Questions & Answers

#### Q9: "Walk me through your development process for this project."

**Your Answer:**
"I followed a structured development approach:

**Phase 1: Requirements Analysis (Day 1)**

- Read the assignment carefully
- Identified key requirements:
  - Object detection
  - Room-based organization
  - Deduplication within rooms
  - Multiple output formats
- Created mental model of solution

**Phase 2: Technology Selection (Day 1-2)**

- Researched object detection models
- Chose YOLOv8 for balance of speed/accuracy
- Selected Flask for web interface (familiar, lightweight)
- Decided on modular architecture for maintainability

**Phase 3: Core Development (Day 2-4)**

- Started with object detection module (most critical)
- Built and tested each module independently
- Followed order:
  1. Object detection (foundation)
  2. Room identification (simple but necessary)
  3. Unique counting (core logic)
  4. Report generation (output)

**Phase 4: CLI Implementation (Day 4-5)**

- Created main.py to tie everything together
- Tested with sample dataset
- Verified output accuracy
- Generated visualizations

**Phase 5: Web Application (Day 5-7)**

- Built Flask routes
- Created HTML templates
- Added file upload functionality
- Tested thoroughly

**Phase 6: UI Polish (Day 7-8)**

- Designed CSS styling
- Made interface responsive
- Added animations and feedback
- Improved user experience

**Phase 7: Documentation (Day 8-9)**

- Wrote comprehensive README
- Added code comments
- Created this technical documentation
- Prepared for presentation

**Key Principles I Followed:**

- Start simple, add complexity gradually
- Test each component before integration
- Keep code modular and reusable
- Think about user experience
- Document as you go"

---

#### Q10: "If you had more time, what would you add?"

**Your Answer:**
"I have several enhancements in mind:

**Immediate Improvements (1-2 weeks):**

1. **Automatic Room Classification**

   - Train/integrate scene classification model
   - Use ResNet or Places365 for room type detection
   - Fall back to metadata if classification confidence is low

2. **Advanced Deduplication**

   - Currently based on class name only
   - Add feature matching for visual similarity
   - Use object embeddings from YOLO for better matching
   - Prevent counting same physical object twice

3. **User Accounts & History**

   - Login system
   - Save processing history
   - Allow users to revisit previous analyses

4. **Batch Processing**
   - Upload entire folders
   - Process video files (frame-by-frame)
   - Show progress with real-time updates

**Medium-term Enhancements (1-2 months):**

5. **API Development**

   - RESTful API for programmatic access
   - Webhook support for async processing
   - API documentation with Swagger

6. **Advanced Analytics**

   - Compare rooms (which has more furniture?)
   - Track changes over time
   - Generate insights (recommended furniture)

7. **Export Options**

   - PDF reports with visualizations
   - Excel files with detailed analytics
   - Shareable links to results

8. **Mobile Application**
   - Native iOS/Android apps
   - Camera integration
   - On-device processing

**Long-term Vision (3-6 months):**

9. **3D Room Reconstruction**

   - Combine with depth estimation
   - Create 3D models of rooms
   - Virtual tours

10. **AR Integration**

    - Augmented reality visualization
    - Place virtual furniture
    - Interior design suggestions

11. **Enterprise Features**

    - Multi-tenant support
    - Team collaboration
    - Custom object training

12. **Performance Optimizations**
    - Model quantization
    - Edge deployment
    - Distributed processing

**Prioritization:**
I would prioritize based on:

1. User impact (what helps users most?)
2. Technical feasibility (what's achievable?)
3. Business value (what drives adoption?)

For immediate next step, I'd add automatic room classification since it aligns with the project goal and provides clear value."

---

## Performance Characteristics

### Time Complexity Analysis

**Object Detection:**

- **Complexity:** O(1) per image (constant model inference time)
- **Actual time:** ~50-200ms per image on CPU
- **Factors:** Image size, model size, hardware

**Room Grouping:**

- **Complexity:** O(n) where n = number of detections
- **Operation:** Single pass to create dictionary
- **Fast:** Just data structure operations

**Unique Counting:**

- **Complexity:** O(n) where n = number of detections per room
- **Set operations:** O(1) average case for add
- **Total:** O(n) for creating set + O(k) for creating dict

**Report Generation:**

- **JSON:** O(n) to serialize dictionary
- **CSV:** O(n × k) where k = average objects per room
- **Negligible:** Compared to detection time

**Visualization:**

- **Complexity:** O(d) per image, where d = number of detections
- **Drawing operations:** Each box + text is O(1)
- **I/O bound:** File writing is the bottleneck

### Space Complexity Analysis

**Model Loading:**

- **YOLOv8n:** ~6MB model size in memory
- **One-time cost:** Loaded once at startup

**Detection Storage:**

- **Per detection:** ~100 bytes (box coordinates, confidence, class name)
- **Per image:** Typically 5-20 detections = ~2KB
- **Per session:** Multiple images = reasonable memory usage

**Report Storage:**

- **JSON:** Compact format, ~1KB per room
- **CSV:** Slightly larger, text-based
- **Visualizations:** Same size as original images

### Optimization Opportunities

1. **Batch Processing:**

   - Current: Sequential image processing
   - Potential: Process multiple images in single model call
   - Benefit: 2-3x throughput improvement

2. **Model Optimization:**

   - Current: Standard FP32 model
   - Potential: INT8 quantization
   - Benefit: 4x faster inference, smaller memory

3. **Caching:**

   - Current: No caching
   - Potential: Cache results by image hash
   - Benefit: Instant results for repeated images

4. **Lazy Loading:**
   - Current: Load all visualizations at once
   - Potential: Load visualizations on demand
   - Benefit: Faster initial page load

---

## Deployment Considerations

### Local Development Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd Lakshya_SimplyPhi

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# 3. Install dependencies
pip install ultralytics opencv-python numpy Pillow Flask Werkzeug

# 4. Run CLI version
python main.py

# 5. Run web version
python app.py
# Navigate to http://127.0.0.1:5000
```

### Production Deployment Options

**Option 1: Simple VPS (DigitalOcean, Linode)**

```bash
# Using Gunicorn as WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

**Option 2: Docker Container**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

**Option 3: Cloud Platform (AWS, Azure, GCP)**

- Use Elastic Beanstalk (AWS) or App Service (Azure)
- Auto-scaling based on traffic
- Managed infrastructure

### Environment Variables

```python
# config.py (production addition)
import os

class Config:
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', 'output')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', 16 * 1024 * 1024))
    MODEL_PATH = os.getenv('MODEL_PATH', 'yolov8n.pt')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

---

## Conclusion

This project demonstrates:

✅ **Technical Skills:**

- Computer vision and deep learning
- Object detection with YOLOv8
- Web development with Flask
- Python programming best practices
- Software architecture design

✅ **Problem-Solving:**

- Breaking down complex requirements
- Choosing appropriate algorithms
- Handling edge cases
- Security considerations

✅ **User Focus:**

- Dual interfaces (CLI + Web)
- Multiple output formats
- Visual feedback
- Clean, professional UI

✅ **Production Awareness:**

- Modular, maintainable code
- Security measures
- Scalability considerations
- Documentation

This system successfully solves the room-wise unique object detection problem and is ready for real-world application with minor enhancements.

---

## Additional Resources

**Further Reading:**

- YOLOv8 Documentation: https://docs.ultralytics.com/
- Flask Documentation: https://flask.palletsprojects.com/
- OpenCV Documentation: https://docs.opencv.org/

**Related Concepts:**

- Object tracking (for video analysis)
- Instance segmentation (for more precise object boundaries)
- Scene classification (for automatic room detection)
- Transfer learning (for custom object categories)

---

**End of Technical Documentation**

_Good luck with your interview! You've built something impressive._
