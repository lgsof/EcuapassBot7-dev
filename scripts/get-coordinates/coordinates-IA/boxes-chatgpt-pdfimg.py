import fitz  # PyMuPDF
import cv2
import numpy as np

def extract_boxes_opencv(pdf_path, dpi=200):
	# Step 1: Render PDF page to image
	doc = fitz.open(pdf_path)
	page = doc.load_page(0)  # First page
	pix = page.get_pixmap(dpi=dpi)
	img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
	print ("+++ pix:", pix)
	cv2.imwrite("rendered_page.png", img)

	if pix.n == 4:	# handle alpha
		img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

	# Step 2: Convert to grayscale & threshold
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

	# Step 3: Find contours
	contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	boxes = []
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		if w > 10 and h > 10:  # filter tiny noise
			boxes.append((x, y, w, h))

	boxes.sort(key=lambda b: (b[1], b[0]))	# top-to-bottom, left-to-right
	return boxes

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print("Usage: python detect_boxes_opencv.py <pdf_file>")
		sys.exit(1)

	path = sys.argv[1]
	boxes = extract_boxes_opencv(path)

	for i, (x, y, w, h) in enumerate(boxes, 1):
		print(f"Box {i}: X={x}, Y={y}, W={w}, H={h}")

