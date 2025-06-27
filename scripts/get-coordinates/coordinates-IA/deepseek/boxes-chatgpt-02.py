import cv2
import numpy as np
from operator import itemgetter

def detect_form_boxes(image_path, output_path=None, min_area=100, max_aspect_ratio=10, 
                      min_width=10, min_height=10, threshold=240):
    """
    Detect rectangular boxes in a PNG image from a PDF form.
    
    Args:
        image_path (str): Path to the input PNG image
        output_path (str, optional): If provided, saves the image with detected boxes
        min_area (int): Minimum area for a contour to be considered a box
        max_aspect_ratio (float): Maximum aspect ratio (width/height) for a box
        min_width (int): Minimum width of a box
        min_height (int): Minimum height of a box
        threshold (int): Threshold value for binarization (0-255)
        
    Returns:
        list: List of boxes as dictionaries with x, y, w, h, ordered top-left to bottom-right
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image from path: " + image_path)
    
    # Convert to grayscale and apply threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    
    # Use morphological operations to enhance box edges
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    detected_boxes = []
    
    for contour in contours:
        # Get the bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calculate area and aspect ratio
        area = w * h
        aspect_ratio = max(w, h) / min(w, h) if min(w, h) > 0 else 0
        
        # Filter based on size and shape
        if (area >= min_area and 
            aspect_ratio <= max_aspect_ratio and
            w >= min_width and 
            h >= min_height):
            
            detected_boxes.append({
                'x': x,
                'y': y,
                'width': w,
                'height': h
            })
    
    # Sort boxes from top-left to bottom-right (top-to-bottom, then left-to-right)
    detected_boxes.sort(key=itemgetter('y', 'x'))
    
    # If output path is provided, draw the boxes on the image
    if output_path:
        for box in detected_boxes:
            x, y, w, h = box['x'], box['y'], box['width'], box['height']
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.imwrite(output_path, image)
    
    return detected_boxes

if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python form_box_extractor.py <input_image.png> [output_image.png]")
        print("Optional parameters can be modified in the script:")
        print("min_area=100, max_aspect_ratio=10, min_width=10, min_height=10, threshold=240")
        sys.exit(1)
    
    input_image = sys.argv[1]
    output_image = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        boxes = detect_form_boxes(input_image, output_image)
        print(f"Detected {len(boxes)} boxes (top-left to bottom-right order):")
        print(json.dumps(boxes, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
