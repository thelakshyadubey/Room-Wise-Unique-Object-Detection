import os
from ultralytics import YOLO
import cv2

class ObjectDetector:
    def __init__(self, model_name='yolov8n.pt'):
        """
        Initializes the ObjectDetector with a YOLOv8 model.
        Args:
            model_name (str): Name of the YOLOv8 model to use (e.g., 'yolov8n.pt', 'yolov8s.pt').
        """
        self.model = YOLO(model_name)
        self.class_names = self.model.names

    def detect_objects(self, image_path):
        """
        Detects objects in an image.
        Args:
            image_path (str): Path to the input image.
        Returns:
            list: A list of dictionaries, where each dictionary contains 'box' (bounding box coordinates),
                  'confidence' (detection confidence), and 'class_name' (name of the detected object).
        """
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at {image_path}")
            return []

        results = self.model(image_path)
        detections = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = round(float(box.conf[0]), 2)
                class_id = int(box.cls[0])
                class_name = self.class_names[class_id]
                detections.append({
                    "box": [x1, y1, x2, y2],
                    "confidence": confidence,
                    "class_name": class_name
                })
        return detections

    def draw_boxes(self, image_path, detections, output_path=None):
        """
        Draws bounding boxes and labels on the image.
        Args:
            image_path (str): Path to the input image.
            detections (list): List of detected objects from detect_objects method.
            output_path (str, optional): Path to save the output image with bounding boxes. If None, displays the image.
        """
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not load image from {image_path}")
            return

        for det in detections:
            x1, y1, x2, y2 = det['box']
            class_name = det['class_name']
            confidence = det['confidence']

            color = (0, 255, 0) # Green color for bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, f"{class_name} {confidence}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        if output_path:
            cv2.imwrite(output_path, img)
            print(f"Detection image saved to {output_path}")
        else:
            cv2.imshow("Detections", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == '__main__':
    # Example Usage (will be replaced by main processing pipeline later)
    # For testing, you might need to place a sample image in the same directory
    # or provide a full path.
    detector = ObjectDetector()
    sample_image_path = "Lakshya_SimplyPhi/sample_image.jpg" # Placeholder
    # if you have a sample image, uncomment and run:
    # detections = detector.detect_objects(sample_image_path)
    # print(detections)
    # detector.draw_boxes(sample_image_path, detections)
