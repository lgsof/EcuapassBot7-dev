#!/usr/bin/env python3

import cv2, sys
import numpy as np
import pytesseract

def detect_lines_with_ocr(pdf_path, page_num=0):
    # Convert PDF to image
    from pdf2image import convert_from_path
    images = convert_from_path(pdf_path)
    img = images[page_num]

    # Convert PIL image to OpenCV format
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Detect lines using pytesseract
    data = pytesseract.image_to_boxes(img)
    lines = [d for d in data.splitlines() if "line" in d.lower()]
    return lines

pdf_path = sys.argv [1]
lines = detect_lines_with_ocr(pdf_path)
print("Detected Lines:", lines)

