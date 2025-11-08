import os
import json
from collections import defaultdict
from object_detector import ObjectDetector
from room_identifier import RoomIdentifier
from unique_object_counter import UniqueObjectCounter
from report_generator import ReportGenerator

def main(dataset_path="Lakshya_SimplyPhi/sample_dataset", output_dir="Lakshya_SimplyPhi/output"):
    """
    Main function to run the room-wise unique object detection pipeline.
    Args:
        dataset_path (str): Path to the directory containing images and metadata.json.
        output_dir (str): Directory to save reports and visualized images.
    """
    print("Starting unique object detection pipeline...")

    # Initialize components
    detector = ObjectDetector()
    room_identifier = RoomIdentifier()
    unique_counter = UniqueObjectCounter()
    report_generator = ReportGenerator()

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "visualizations"), exist_ok=True)

    # Load metadata
    metadata_path = os.path.join(dataset_path, "metadata.json")
    if not os.path.exists(metadata_path):
        print(f"Error: metadata.json not found at {metadata_path}")
        return
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    all_detections_by_room = defaultdict(list)
    all_detections_with_boxes_by_room = defaultdict(list)

    # Process each image in the dataset
    for image_name, img_metadata in metadata.items():
        image_path = os.path.join(dataset_path, image_name)
        print(f"\nProcessing image: {image_name}")

        # 1. Room Identification
        room_id = room_identifier.get_room_id(img_metadata)
        if not room_id:
            print(f"Warning: No room ID found for {image_name}. Skipping.")
            continue
        print(f"Identified Room ID: {room_id}")

        # 2. Object Detection
        detections = detector.detect_objects(image_path)
        print(f"Detected objects: {[d['class_name'] for d in detections]}")

        all_detections_by_room[room_id].extend(detections)
        all_detections_with_boxes_by_room[room_id].append({
            "image_name": image_name,
            "image_path": image_path,
            "detections": detections
        })

        # Optional: Visualize and save detections for each image
        output_image_path = os.path.join(output_dir, "visualizations", f"detected_{image_name}")
        report_generator.visualize_detections(image_path, detections, output_image_path)

    # 3. Unique Object Counting
    unique_counts = unique_counter.count_unique_objects(all_detections_by_room)
    print("\nUnique object counts per room:", unique_counts)

    # 4. Room-wise Report Generation
    json_report_path = os.path.join(output_dir, "room_wise_report.json")
    csv_report_path = os.path.join(output_dir, "room_wise_report.csv")
    report_generator.generate_json_report(unique_counts, json_report_path)
    report_generator.generate_csv_report(unique_counts, csv_report_path)

    print("\nPipeline finished. Reports and visualizations are in the 'output' directory.")

if __name__ == '__main__':
    # This part remains for command-line execution of the pipeline
    # To run the web interface, execute `python app.py`
    main(dataset_path="sample_dataset", output_dir="output")
