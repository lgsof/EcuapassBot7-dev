#!/usr/bin/env python3
import sys, json
import pdfplumber
import fitz  # PyMuPDF

#--------------------------------------------------------------------
# 1. Detect Horizontal and Vertical Lines
# Extract the lines using pdfplumber and classify them:
#--------------------------------------------------------------------
def main():
	args = sys.argv
	pdfFile = "CPI-SANCHEZPOLO-061984-24.pdf"

	boxes = detectBoxes (pdfFile, 0.01)
	outPdf = drawBoxesOnPdf (pdfFile, boxes, WIDTH=3, COLORBOX=(1,0,0), COLORTEXT=(1,1,0))

	textBoxes = getTextBoxes (boxes)
	#pdfFileBoxes = "CPI-SANCHEZPOLO-061984-24-BOXES.pdf"
	#drawBoxesOnPdf (outPdf, textBoxes, COLORBOX=(0,0,1), COLORTEXT=(0,0,1))

	# Save coordinates
	#saveTxtCoords (textBoxes, pdfFile)
	saveJsonCoords (textBoxes, pdfFile)

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def saveJsonCoords (textBoxes, filename):
	outFilename = f"{filename.split('.')[0]}-coordinates.json"
	with open (outFilename, "w") as fp:
		json.dump (textBoxes, fp, indent=4)
#--------------------------------------------------------------------
#--------------------------------------------------------------------
def saveTxtCoords (textBoxes, filename):
	outFilename = f"{filename.split('.')[0]}-coordinates.txt"
	outFile = open (outFilename, "w")
	for k,v in textBoxes.items ():
		v = [int (x) for x in v]
		name = k.replace ("txt", "")
		outFile.write (f"{name}:{v[0]},{v[1]},{v[2]},{v[3]}\n")
	outFile.close ()
#--------------------------------------------------------------------
#--------------------------------------------------------------------
def detectBoxes (pdf_path, tolerance=1):
	doc = fitz.open(pdf_path)
	page = doc[0]

	# Retrieve all drawing commands
	shapes = page.get_drawings()

	boxes = []
	for k, shape in enumerate (shapes):
		for i, item in enumerate (shape["items"]):
			if item[0] == "re":	# Check if the item is a line
				boxes.append (item [1])
	return boxes

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def printBoxes (boxes):
	for i, box in enumerate (boxes):
		print (f"Box {i} : {box}")
		print ("")

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def drawBoxesOnPdf (pdfFilename, boxes, WIDTH=1, COLORBOX=(0,0,1), COLORTEXT=(1,0,1)):
	if type (boxes) is list:
		boxes = {str (i):x for i,x in enumerate (boxes)}

	# Open the PDF
	output_pdf  = pdfFilename.split (".")[0] + "-BOXES.pdf"

	pdf_document = fitz.open(pdfFilename)

	# Draw a rectangle on the first page
	page = pdf_document[0]
	for k, box in boxes.items():
		text = str (k).zfill(2)
		rect = fitz.Rect (box)  # (x0, y0, x1, y1)
		page.draw_rect (rect, color=COLORBOX, width=WIDTH)  # Red border
		page.insert_text ((box[0]+5, box[1]+15), text, fontsize=16, color=COLORTEXT)  # Blue text

	# Save the modified PDF
	pdf_document.save(output_pdf)
	pdf_document.close()
	return output_pdf

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def getTextBoxes (boxes):
	b = boxes
	coords = {}
	coords ["txt0a"]   = boxSimple (b[1])
	coords ["txt00"]   = boxSimple (b[1])
	coords ["txt01"]   = boxLabel (b[2])
	coords ["txt02"]   = boxLabel (b[4])
	coords ["txt03"]   = boxLabel (b[7])
	coords ["txt04"]   = boxLabel (b[10])
	coords ["txt05"]   = boxLabel (b[3])
	coords ["txt06"]   = boxLabel (b[5])
	coords ["txt07"]   = boxLabel (b[6])
	coords ["txt08"]   = boxLabel (b[8])
	coords ["txt09"]   = boxLabel (b[9])
	coords ["txt10"]   = boxMercancia (b[11], b[19])
	coords ["txt11"]   = boxMercancia (b[12], b[19])
	coords ["txt12"]   = boxMercancia (b[13], b[19])
	coords ["txt13_1"] = boxLabel (b[15])
	coords ["txt13_2"] = boxLabel (b[16])
	coords ["txt14"]   = boxLabel (b[17])
	coords ["txt15"]   = boxLabel (b[18])
	coords ["txt16"]   = boxIncoterms (b[17], b[18], b[20])
	coords ["txt17_11"]  = boxGastos (b[22], 0)
	coords ["txt17_12"]  = boxGastos (b[22], 1)
	coords ["txt17_13"]  = boxGastos (b[22], 2)
	coords ["txt17_14"]  = boxGastos (b[22], 3)
	coords ["txt17_31"]  = boxGastos (b[24], 0)
	coords ["txt17_32"]  = boxGastos (b[24], 1)
	coords ["txt17_33"]  = boxGastos (b[24], 2)
	coords ["txt17_34"]  = boxGastos (b[24], 3)
	coords ["txt18"]   = boxLabel (b[27])
	coords ["txt19"]   = boxLabel (b[29])
	coords ["txt20"]   = boxLabel (b[30])
	coords ["txt21"]   = boxLabel (b[20])
	coords ["txt22"]   = boxLabel (b[28])

	coordsDic = {}
	for k, v in coords.items ():
		coordsDic [k] = [int (x) for x in [v[0],v[1],v[2],v[3]]]

	return coordsDic

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def boxSimple (box):
	return box

def boxLabel (box):
	box [1] += 9
	return box

def boxMercancia (boxTop, boxBottom):
	box = (boxTop [0], boxTop [3], boxTop [2], boxBottom [1])
	return box

def boxIncoterms (boxTop1, boxTop2, boxBottom):
	box = (boxTop1 [0], boxTop1 [3] + 18, boxTop2 [2], boxBottom [1])
	return box

def boxGastos (boxTop, rowNumber):
	rowSize = 24 if rowNumber !=3 else 14
	rowPos  = boxTop[3] + rowNumber * 24
	box = (boxTop [0], rowPos , boxTop [2], rowPos + rowSize)
	return box

#--------------------------------------------------------------------
#--------------------------------------------------------------------
main ()

