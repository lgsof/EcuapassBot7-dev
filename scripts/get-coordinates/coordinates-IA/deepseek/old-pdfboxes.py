import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTFigure, LTRect
from pdf2image import convert_from_path
import cv2
import numpy as np

def detect_pdf_form_fields(pdf_path, output_image_path=None):
    """
    Detect form fields directly from PDF structure and optionally visualize on rendered image.
    
    Args:
        pdf_path: Path to the PDF file
        output_image_path: Optional path to save visualization image
    
    Returns:
        List of detected form fields with coordinates and dimensions
    """
    # Extract form fields from PDF structure
    form_fields = []
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTRect):
                # Check if rectangle might be a form field
                if element.width > 10 and element.height > 10:  # Filter small elements
                    form_fields.append({
                        'x': element.x0,
                        'y': element.y1,  # PDF coordinates have y increasing upward
                        'width': element.width,
                        'height': element.height,
                        'page': page_layout.pageid
                    })
    
    # If we want to visualize on rendered image
    if output_image_path:
        # Convert first page to image
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        if images:
            image = np.array(images[0])
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Draw detected boxes
            for field in [f for f in form_fields if f['page'] == 1]:
                x, y = int(field['x']), int(field['y'])
                w, h = int(field['width']), int(field['height'])
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            cv2.imwrite(output_image_path, image)
    
    return form_fields

if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_form_detector.py <input.pdf> [output_image.png]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_image = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        fields = detect_pdf_form_fields(pdf_file, output_image)
        print(f"Detected {len(fields)} form fields:")
        print(json.dumps(fields, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
