import cv2
import numpy as np
from operator import itemgetter

def detect_form_boxes(image_path, output_path=None, 
                     min_line_length=50, max_line_gap=10, 
                     kernel_size=3, iterations=1):
    """
    Detect form boxes by finding horizontal and vertical lines and their intersections.
    
    Args:
        image_path (str): Path to the input PNG image
        output_path (str, optional): Output image with detected boxes
        min_line_length (int): Minimum length of line segments to detect
        max_line_gap (int): Maximum gap between line segments to treat as single line
        kernel_size (int): Size of kernel for morphological operations
        iterations (int): Number of iterations for morphological operations
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image from path: " + image_path)
    
    # Convert to grayscale and threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Morphological operations to enhance lines
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=iterations)
    
    # Detect lines using HoughLinesP
    lines = cv2.HoughLinesP(dilated, 1, np.pi/180, 100, 
                           minLineLength=min_line_length, 
                           maxLineGap=max_line_gap)
    
    if lines is None:
        return []
    
    # Separate horizontal and vertical lines
    horizontal = []
    vertical = []
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y2 - y1) < 5:  # Horizontal line
            horizontal.append((min(y1, y2), max(y1, y2), min(x1, x2), max(x1, x2)))
        elif abs(x2 - x1) < 5:  # Vertical line
            vertical.append((min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)))
    
    # Find intersections to form boxes
    boxes = []
    for h in horizontal:
        for v in vertical:
            # Check if lines intersect
            if (v[0] >= h[2] and v[0] <= h[3] and 
                h[0] >= v[2] and h[0] <= v[3]):
                # Potential box corner
                for h2 in horizontal:
                    for v2 in vertical:
                        if (v2[0] >= h2[2] and v2[0] <= h2[3] and 
                            h2[0] >= v2[2] and h2[0] <= v2[3] and
                            v[0] < v2[0] and h[0] < h2[0]):
                            # Found a box
                            x = v[0]
                            y = h[0]
                            w = v2[0] - v[0]
                            h_box = h2[0] - h[0]
                            boxes.append({'x': x, 'y': y, 'width': w, 'height': h_box})
    
    # Remove duplicate boxes
    unique_boxes = []
    seen = set()
    for box in boxes:
        box_tuple = (box['x'], box['y'], box['width'], box['height'])
        if box_tuple not in seen:
            seen.add(box_tuple)
            unique_boxes.append(box)
    
    # Sort boxes from top-left to bottom-right
    unique_boxes.sort(key=itemgetter('y', 'x'))
    
    # Draw boxes if output path specified
    if output_path:
        for box in unique_boxes:
            x, y, w, h = box['x'], box['y'], box['width'], box['height']
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite(output_path, image)
    
    return unique_boxes

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
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
