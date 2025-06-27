#!/usr/bin/env python3
import sys, json
import pdfplumber

#--------------------------------------------------------------------
# 1. Detect Horizontal and Vertical Lines
# Extract the lines using pdfplumber and classify them:
#--------------------------------------------------------------------
import fitz  # PyMuPDF

def detect_horizontal_lines_with_fitz (pdf_path, tolerance=1):
	doc = fitz.open(pdf_path)
	page = doc[0]

	# Retrieve all drawing commands
	shapes = page.get_drawings()

	horizontal_lines = []
	for k, shape in enumerate (shapes):
		for i, item in enumerate (shape["items"]):
			if item[0] == "re":	# Check if the item is a line
				print (f"Item {k}-{i}:", item)
			continue
			if item[0] == "l":	# Check if the item is a line
				print ("item 0:", item [1][0])
				(x0, y0), (x1, y1) = item [1], item[2]
				if abs(y0 - y1) <= tolerance:  # Nearly horizontal
					horizontal_lines.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1})

	return horizontal_lines

def getLinesFromPDF (pdf_path):
	doc = fitz.open (pdf_path)
	page = doc[0]

	# Retrieve all drawing commands
	shapes = page.get_drawings()

	horizontal_lines = []
	for k, shape in enumerate (shapes):
		for i, item in enumerate (shape["items"]):
			#print (f"Item {k}-{i}:", item)
			if item[0] == "l":	# Check if the item is a line
				(x0, y0), (x1, y1) = item [1], item[2]
				horizontal_lines.append ((y0, x0, y1, x1))
			if item[0] == "re":  # Check if the item is a line
				x0, y0, x1, y1 = item [1]
				horizontal_lines.append ((y0, x0, y0, x1))
				horizontal_lines.append ((y1, x0, y1, x1))

	hLines = []
	sorted_lines = sorted (horizontal_lines, key=lambda x: x[0])
	ly0 = 0
	lx0 = 0
	for i in range (len (sorted_lines[:-1])):
		y0 = sorted_lines [i][0]
		x0 = sorted_lines [i][1]
		print (f"Adding: {y0}-{ly0} and {x0}-{lx0}")
		if abs(y0 - ly0) < 2 and abs (lx0 - x0) >= 2 :  # Nearly horizontal
			print (f">>> Adding: {y0}-{ly0} and {x0}-{lx0}")
			hLines.append (sorted_lines [i])
		ly0 = y0
		lx0 = x0

	return hLines

def detect_lines(pdf_path):
	with pdfplumber.open(pdf_path) as pdf:
		page = pdf.pages[0]  # Analyze the first page
		lines = page.lines	# Get all detected lines

		for i, line in enumerate (lines):
			print (f"Line {i} : {line}")


		# Separate horizontal and vertical lines
		horizontal_lines = [
			line for line in lines if abs(line['y0'] - line['y1']) < 1	# Nearly horizontal
		]
		vertical_lines = [
			line for line in lines if abs(line['x0'] - line['x1']) < 1	# Nearly vertical
		]

		# Convert value to int and 0-starting
		horizontalLines = []
		for line in horizontal_lines:
			line ['y0'] = 841 - int (line ['y0'])
			horizontalLines.append (line)


		return horizontalLines, vertical_lines


#--------------------------------------------------------------------
# 2. Match Lines to Form Boxes
# Match the vertical lines with dynamically detected horizontal lines
#--------------------------------------------------------------------
def detect_boxes (horizontal_lines, vertical_lines, pdf_path):
	boxes = {}
	# Sort lines by their positions
	horizontal_lines = sorted(horizontal_lines, key=lambda line: line['y0'])
	vertical_lines = sorted(vertical_lines, key=lambda line: line['x0'])

	for i in range(len(horizontal_lines) - 1):
		top_line = horizontal_lines[i]
		bottom_line = horizontal_lines[i + 1]
		for left_line in vertical_lines:
			i = 0
			for right_line in vertical_lines:
				if left_line['x0'] >= right_line['x0']:
					continue

				# Check if the lines form a valid rectangle
				if (
					left_line['x0'] >= top_line['x0'] <= right_line['x0']
					and left_line['x0'] >= bottom_line['x0'] <= right_line['x0']
					and top_line['y0'] < bottom_line['y0']
				):
					box = {
						"x0": int (left_line['x0']),
						"y0": int (top_line['y0']),
						"x1": int (right_line['x0']),
						"y1": int (bottom_line['y0']),
					}
					#boxes.append(box)
					key = f"box{str(i).zfill(2)}"
					boxes [key] = box
					i += 1
	boxesToJson (boxes, pdf_path)
	return boxes

def boxesToJson (boxes, filename):
	outFile = filename.split(".")[0]+"-BOXES.json"
	json.dump (boxes, open (outFile, "w"), indent=4)

#--------------------------------------------------------------------
#--------------------------------------------------------------------
args = sys.argv
pdf_path = args [1]

# 1. Dectect horizontal and vertical lines
#horizontal_lines, vertical_lines = detect_lines(pdf_path)
horizontal_lines = detect_horizontal_lines_with_fitz (pdf_path, 0.01)
#horizontal_lines = getLinesFromPDF (pdf_path)
#for i, line in enumerate (horizontal_lines):
#	print (f"Line {i} : {line}")


