import fitz  # PyMuPDF
import numpy as np
from collections import defaultdict

def detect_boxes_from_pdf(pdf_path, output_image_path=None):
    """
    Detect form boxes directly from PDF by analyzing lines and rectangles.
    
    Args:
        pdf_path: Path to input PDF file
        output_image_path: Optional path to save visualization image
    
    Returns:
        List of detected boxes [x, y, width, height, page_num]
    """
    doc = fitz.open(pdf_path)
    boxes = []
    
    for page_num, page in enumerate(doc, start=1):
        # Get all paths (lines, rectangles) on the page
        paths = page.get_drawings()
        
        # Collect horizontal and vertical lines
        h_lines = defaultdict(list)  # key: y-coordinate, value: list of x-ranges
        v_lines = defaultdict(list)  # key: x-coordinate, value: list of y-ranges
        
        for path in paths:
            for item in path["items"]:
                # Handle lines
                if item[0] == "l":  # Line item
                    points = item[1]  # Get the points tuple
                    x1, y1, x2, y2 = points
                    if abs(x1 - x2) < 2:  # Vertical line
                        v_lines[round(x1, 1)].append((round(min(y1, y2), 1), round(max(y1, y2), 1)))
                    elif abs(y1 - y2) < 2:  # Horizontal line
                        h_lines[round(y1, 1)].append((round(min(x1, x2), 1), round(max(x1, x2), 1)))
                
                # Handle rectangles
                elif item[0] == "re":  # Rectangle item
                    rect = item[1]  # Get the rectangle tuple
                    x, y, w, h = rect
                    if w > 5 and h > 5:  # Filter tiny rectangles
                        boxes.append({
                            "x": x,
                            "y": y,
                            "width": w,
                            "height": h,
                            "page": page_num,
                            "type": "rectangle"
                        })
        
        # Find boxes from line intersections
        for y in h_lines:
            for x_start, x_end in h_lines[y]:
                for x in v_lines:
                    if x_start <= x <= x_end:
                        for y_bottom in h_lines:
                            if y_bottom > y:  # Find bottom boundary
                                for x_start2, x_end2 in h_lines[y_bottom]:
                                    if x_start <= x <= x_end:
                                        # Check if vertical lines connect top and bottom
                                        for y_range in v_lines[x]:
                                            if y_range[0] <= y and y_range[1] >= y_bottom:
                                                boxes.append({
                                                    "x": x_start,
                                                    "y": y,
                                                    "width": x_end - x_start,
                                                    "height": y_bottom - y,
                                                    "page": page_num,
                                                    "type": "constructed"
                                                })
    
    # Remove duplicate boxes (round to 1 decimal place for comparison)
    unique_boxes = []
    seen = set()
    
    for box in boxes:
        key = (
            round(box["x"], 1),
            round(box["y"], 1),
            round(box["width"], 1),
            round(box["height"], 1),
            box["page"]
        )
        if key not in seen:
            seen.add(key)
            unique_boxes.append(box)
    
    # Optional visualization
    if output_image_path:
        visualize_boxes(doc, unique_boxes, output_image_path)
    
    return unique_boxes

def visualize_boxes(doc, boxes, output_prefix):
    """Generate visualization of detected boxes"""
    import cv2
    
    for page_num in sorted({b["page"] for b in boxes}):
        page = doc[page_num - 1]  # Pages are 0-indexed
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, 3)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        for box in [b for b in boxes if b["page"] == page_num]:
            x, y = int(box["x"]), int(box["y"])
            w, h = int(box["width"]), int(box["height"])
            color = (0, 255, 0) if box.get("type") == "rectangle" else (0, 0, 255)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        
        cv2.imwrite(f"{output_prefix}_page{page_num}.png", img)

if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_box_detector.py <input.pdf> [output_prefix]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    try:
        boxes = detect_boxes_from_pdf(pdf_file, output_prefix)
        print(f"Detected {len(boxes)} form boxes:")
        print(json.dumps(boxes, indent=2))
        
        if not boxes:
            print("\nNo boxes detected. Possible reasons:")
            print("- The PDF doesn't contain visible vector lines/rectangles")
            print("- The form uses non-standard elements")
            print("- Try increasing the rounding tolerance in the code")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
