import json
import csv
import os
import cv2

class ReportGenerator:
    def __init__(self):
        """
        Initializes the ReportGenerator.
        """
        pass

    def generate_json_report(self, unique_counts_by_room, output_filepath):
        """
        Generates a JSON report of unique object counts per room.
        Args:
            unique_counts_by_room (dict): Dictionary of unique object counts by room.
            output_filepath (str): Path to save the JSON report.
        """
        with open(output_filepath, 'w') as f:
            json.dump(unique_counts_by_room, f, indent=4)
        print(f"JSON report saved to {output_filepath}")

    def generate_csv_report(self, unique_counts_by_room, output_filepath):
        """
        Generates a CSV report of unique object counts per room.
        Args:
            unique_counts_by_room (dict): Dictionary of unique object counts by room.
            output_filepath (str): Path to save the CSV report.
        """
        with open(output_filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Room ID", "Object", "Count"])
            for room_id, objects in unique_counts_by_room.items():
                for obj_name, count in objects.items():
                    writer.writerow([room_id, obj_name, count])
        print(f"CSV report saved to {output_filepath}")

    def visualize_detections(self, image_path, detections, output_path=None):
        """
        Draws bounding boxes and labels on the image and saves or displays it.
        Args:
            image_path (str): Path to the input image.
            detections (list): List of detected objects.
            output_path (str, optional): Path to save the output image. If None, displays it.
        """
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not load image from {image_path}")
            return

        for det in detections:
            x1, y1, x2, y2 = det['box']
            class_name = det['class_name']
            confidence = det['confidence']

            color = (0, 255, 0)  # Green color for bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, f"{class_name} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        if output_path:
            cv2.imwrite(output_path, img)
            print(f"Detection image saved to {output_path}")
        else:
            cv2.imshow("Detections", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == '__main__':
    # Example Usage
    generator = ReportGenerator()

    sample_unique_counts = {
        "Room A": {"Sofa": 1, "Chair": 1, "TV": 1},
        "Room B": {"TV": 1}
    }

    # Test JSON report generation
    json_output_path = "Lakshya_SimplyPhi/report.json"
    generator.generate_json_report(sample_unique_counts, json_output_path)

    # Test CSV report generation
    csv_output_path = "Lakshya_SimplyPhi/report.csv"
    generator.generate_csv_report(sample_unique_counts, csv_output_path)

    # Example for visualization (requires a dummy image and detections)
    # For real usage, you would pass actual image_path and detections from object_detector
    # dummy_image_path = "Lakshya_SimplyPhi/sample_image.jpg" # Ensure this image exists for testing
    # dummy_detections = [
    #     {"box": [50, 50, 150, 150], "confidence": 0.9, "class_name": "Sofa"},
    #     {"box": [200, 200, 300, 300], "confidence": 0.8, "class_name": "Chair"}
    # ]
    # if os.path.exists(dummy_image_path):
    #     generator.visualize_detections(dummy_image_path, dummy_detections, "Lakshya_SimplyPhi/visualized_sample.jpg")
    # else:
    #     print(f"Dummy image not found at {dummy_image_path}. Skipping visualization example.")
