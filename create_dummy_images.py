import cv2
import numpy as np
import os

def create_dummy_image(filepath, width=640, height=480, color=(255, 255, 255)):
    """
    Creates a blank dummy image with the specified dimensions and color.
    Args:
        filepath (str): The path to save the image.
        width (int): Width of the image.
        height (int): Height of the image.
        color (tuple): BGR color tuple for the image (default is white).
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = color
    cv2.imwrite(filepath, img)
    print(f"Dummy image created at: {filepath}")

if __name__ == '__main__':
    # The script is assumed to be run from the project root (C:\Users\Lakshya Dubey\Lakshya_SimplyPhi)
    dataset_dir = "sample_dataset"
    os.makedirs(dataset_dir, exist_ok=True)

    create_dummy_image(os.path.join(dataset_dir, "image1.jpg"))
    create_dummy_image(os.path.join(dataset_dir, "image2.jpg"))
    create_dummy_image(os.path.join(dataset_dir, "image3.jpg"))
    create_dummy_image(os.path.join(dataset_dir, "image4.jpg"))
