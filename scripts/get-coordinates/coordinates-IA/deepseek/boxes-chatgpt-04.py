import cv2
import numpy as np
from operator import itemgetter

def detect_form_boxes(image_path, output_path=None):
    """
    Enhanced form box detection using multiple techniques.
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image from path: " + image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Try multiple thresholding methods
    for threshold_method in [
        lambda g: cv2.threshold(g, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU),
        lambda g: cv2.threshold(g, 240, 255, cv2.THRESH_BINARY_INV),
        lambda g: (cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY_INV, 11, 2), 0)
    ]:
        try:
            _, thresh = threshold_method(gray)
            
            # Try both contour detection methods
            for contours_method in [
                lambda t: cv2.findContours(t, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE),
                lambda t: cv2.findContours(t, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            ]:
                contours, _ = contours_method(thresh.copy())
                
                detected_boxes = []
                for contour in contours:
                    # Simplify contour
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    
                    # Get bounding rect
                    x, y, w, h = cv2.boundingRect(approx)
                    
                    # Filter very small detections
                    if w > 10 and h > 10:
                        detected_boxes.append({
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h
                        })
                
                if len(detected_boxes) > 1:  # Found multiple boxes
                    # Sort boxes from top-left to bottom-right
                    detected_boxes.sort(key=itemgetter('y', 'x'))
                    
                    # Draw results if output path specified
                    if output_path:
                        result = image.copy()
                        for box in detected_boxes:
                            cv2.rectangle(result, 
                                         (box['x'], box['y']), 
                                         (box['x'] + box['width'], box['y'] + box['height']), 
                                         (0, 255, 0), 2)
                        cv2.imwrite(output_path, result)
                    
                    return detected_boxes
                    
        except:
            continue
    
    return []  # Return empty if no boxes found

if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python form_box_extractor.py <input_image.png> [output_image.png]")
        sys.exit(1)
    
    input_image = sys.argv[1]
    output_image = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        boxes = detect_form_boxes(input_image, output_image)
        print(f"Detected {len(boxes)} boxes (top-left to bottom-right order):")
        print(json.dumps(boxes, indent=2))
        
        if len(boxes) == 0:
            print("\nTIPS: If no boxes were detected, try:")
            print("1. Checking if the boxes are visible in the image")
            print("2. Converting the PDF to a higher resolution PNG")
            print("3. Trying a different threshold method in the code")
            print("4. Pre-processing the image to enhance box edges")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
