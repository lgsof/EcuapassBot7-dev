#!/usr/bin/env python3
import sys, json
import pdfplumber
import fitz  # PyMuPDF

#--------------------------------------------------------------------
# 1. Detect Horizontal and Vertical Lines
# Extract the lines using pdfplumber and classify them:
#--------------------------------------------------------------------
def main ():
	fullTest ()

def simpleTest ():
	args = sys.argv
	pdfFile = "CPI-SANCHEZPOLO-061984-24.pdf"
	getPdfCoordinates (pdfFile)

def fullTest():
	args = sys.argv
	pdfFile = "CPI-SANCHEZPOLO-061984-24.pdf"

	pdf    = ScrapingPDF_SANCHEZPOLO ()
	boxes  = pdf.getRawBoxesFromPdf (pdfFile)
	outPdf = pdf.drawBoxesOnPdf (pdfFile, boxes, WIDTH=3, COLORBOX=(1,0,0), COLORTEXT=(1,1,0))

	textBoxes = pdf.getDocumentBoxesFromPdf (boxes)
	#pdfFileBoxes = "CPI-SANCHEZPOLO-061984-24-BOXES.pdf"
	pdf.drawBoxesOnPdf (outPdf, textBoxes, COLORBOX=(0,0,1), COLORTEXT=(0,0,1))

	# Save txt coordinates
	pdf.saveTxtCoords (textBoxes, pdfFile)

#--------------------------------------------------------------------
#--------------------------------------------------------------------
class ScrapingPDF_SANCHEZPOLO:
	#--------------------------------------------------------------------
	# Get from PDF coordinates where text is written (no labels)
	#--------------------------------------------------------------------
	def getPdfCoordinates (self, pdfFilepath):
		rawBoxes = self.getRawBoxesFromPdf (pdfFilepath)
		docBoxes = self.getDocumentBoxesFromPdf (rawBoxes)
		coords   = self.convertBoxesToCoords (docBoxes)

		jsonFilename = pdfFilepath.split (".")[0] + "-COORDS.json"
		json.dump (coords, open (jsonFilename, "w"), indent=4)

		return coords

	#--------------------------------------------------------------------
	# Get raw (all detected) boxes from PDF file
	#--------------------------------------------------------------------
	def getRawBoxesFromPdf (self, pdf_path):
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
	# Get document boxes (containing document text) from PDF file
	#--------------------------------------------------------------------
	def getDocumentBoxesFromPdf (self, boxes):
		b = boxes
		textBoxes = {}
		textBoxes ["txt0b"]     = self.getDocBox ("Simple", b[1])
		textBoxes ["txt0a"]     = self.getDocBox ("Simple", b[1])
		textBoxes ["txt00"]     = self.getDocBox ("Simple", b[1])
		textBoxes ["txt01"]     = self.getDocBox ("Label", b[2])
		textBoxes ["txt02"]     = self.getDocBox ("Label", b[4])
		textBoxes ["txt03"]     = self.getDocBox ("Label", b[7])
		textBoxes ["txt04"]     = self.getDocBox ("Label", b[10])
		textBoxes ["txt05"]     = self.getDocBox ("Label", b[3])
		textBoxes ["txt06"]     = self.getDocBox ("Label", b[5])
		textBoxes ["txt07"]     = self.getDocBox ("Label", b[6])
		textBoxes ["txt08"]     = self.getDocBox ("Label", b[8])
		textBoxes ["txt09"]     = self.getDocBox ("Label", b[9])
		textBoxes ["txt10"]     = self.getDocBox ("Mercancia", b[11], b[19])
		textBoxes ["txt11"]     = self.getDocBox ("Mercancia", b[12], b[19])
		textBoxes ["txt12"]     = self.getDocBox ("Mercancia", b[13], b[19])
		textBoxes ["txt13_1"]   = self.getDocBox ("Label", b[15])
		textBoxes ["txt13_2"]   = self.getDocBox ("Label", b[16])
		textBoxes ["txt14"]     = self.getDocBox ("Label", b[17], 2)
		textBoxes ["txt15"]     = self.getDocBox ("Label", b[18], 2)
		textBoxes ["txt16"]     = self.getDocBox ("Incoterms", b[17], b[18], b[20])
		textBoxes ["txt17_11"]  = self.getDocBox ("Gastos", b[22], 0)
		textBoxes ["txt17_12"]  = self.getDocBox ("Gastos", b[22], 1)
		textBoxes ["txt17_13"]  = self.getDocBox ("Gastos", b[22], 2)
		textBoxes ["txt17_14"]  = self.getDocBox ("Gastos", b[22], 3)

		textBoxes ["txt17_21"]  = self.getDocBox ("Gastos", b[23], 0)
		textBoxes ["txt17_22"]  = self.getDocBox ("Gastos", b[23], 1)
		textBoxes ["txt17_23"]  = self.getDocBox ("Gastos", b[23], 2)
		textBoxes ["txt17_24"]  = self.getDocBox ("Gastos", b[23], 3)
		
		textBoxes ["txt17_31"]  = self.getDocBox ("Gastos", b[24], 0)
		textBoxes ["txt17_32"]  = self.getDocBox ("Gastos", b[24], 1)
		textBoxes ["txt17_33"]  = self.getDocBox ("Gastos", b[24], 2)
		textBoxes ["txt17_34"]  = self.getDocBox ("Gastos", b[24], 3)

		textBoxes ["txt17_41"]  = self.getDocBox ("Gastos", b[25], 0)
		textBoxes ["txt17_42"]  = self.getDocBox ("Gastos", b[25], 1)
		textBoxes ["txt17_43"]  = self.getDocBox ("Gastos", b[25], 2)
		textBoxes ["txt17_44"]  = self.getDocBox ("Gastos", b[25], 3)

		textBoxes ["txt18"]     = self.getDocBox ("Label", b[27])
		textBoxes ["txt19"]     = self.getDocBox ("Label", b[29])
		textBoxes ["txt20"]     = self.getDocBox ("Label", b[30])
		textBoxes ["txt21"]     = self.getDocBox ("Label", b[20])
		textBoxes ["txt22"]     = self.getDocBox ("Simple", b[28])
		textBoxes ["txt23"]     = self.getDocBox ("MRN", b[11], b[12], b[19])

		return textBoxes

	#--------------------------------------------------------------------
	# Convert boxes (Rect type) to coords: x, y, width, height
	#--------------------------------------------------------------------
	def convertBoxesToCoords (boxes):
		coords = {}
		for k, v in boxes.items ():
			coords [k] = [int (x) for x in [v[0],v[1],v[2]-v[0]+1,v[3]-v[1]+1]]
		return coords

	#--------------------------------------------------------------------
	# Get box region containing the specific type of document text
	#--------------------------------------------------------------------
	def getDocBox (self, boxType, *args):
		if boxType == "Simple":
			box = args [0]
			return int (box [0]), int (box [1]), int (box [2]-box[0] + 1), int (box [3] - box [1] + 1)

		elif boxType == "Label":
			box = args [0]
			box [1] += 9*labelLines
			return box

		elif boxType == "Mercancia":
			box = (boxTop [0], boxTop [3], boxTop [2], boxBottom [1]-30)
			return (box)

		elif boxType == "Incoterms":
			box = (boxTop1 [0], boxTop1 [3] + 18, boxTop2 [2], boxBottom [1])
			return (box)

		elif boxType == "Gastos":
			rowSize = 24 if rowNumber !=3 else 14
			rowPos  = boxTop[3] + rowNumber * 24
			box = (boxTop [0], rowPos , boxTop [2], rowPos + rowSize)
			return (box)

		elif boxType == "MRN":
			box = (left [0], bottom [1]-30, right [2], bottom [1]) 
			return box

#	def boxToCoords (box):
#			return int (box [0]), int (box [1]), int (box [2]-box[0] + 1), int (box [3] - box [1] + 1)
#		elif boxType == "Label":
#
#	def boxSimple (box):
#		return (box)
#
#	def boxLabel (box, labelLines=1):
#		box [1] += 9*labelLines
#		return (box)
#
#	def boxMercancia (boxTop, boxBottom):
#		box = (boxTop [0], boxTop [3], boxTop [2], boxBottom [1]-30)
#		return (box)
#
#	def boxIncoterms (boxTop1, boxTop2, boxBottom):
#		box = (boxTop1 [0], boxTop1 [3] + 18, boxTop2 [2], boxBottom [1])
#		return (box)
#
#	def boxGastos (boxTop, rowNumber):
#		rowSize = 24 if rowNumber !=3 else 14
#		rowPos  = boxTop[3] + rowNumber * 24
#		box = (boxTop [0], rowPos , boxTop [2], rowPos + rowSize)
#		return (box)
#
#	def boxMRN (left, right, bottom):
#		box = (left [0], bottom [1]-30, right [2], bottom [1]) 
#		return box

	#--------------------------------------------------------------------
	#--------------------------------------------------------------------
	def saveTxtCoords (self, textBoxes, filename):
		outFilename = f"{filename.split('.')[0]}-coordinates.txt"
		outFile = open (outFilename, "w")
		for k,v in textBoxes.items ():
			v = [int (x) for x in v]
			name = k.replace ("txt", "")
			outFile.write (f"{name}:{v[0]},{v[1]},{v[2]},{v[3]}\n")
		outFile.close ()
	#--------------------------------------------------------------------
	#--------------------------------------------------------------------
	def printBoxes (self, boxes):
		for i, box in enumerate (boxes):
			print (f"Box {i} : {box}")
			print ("")

	#--------------------------------------------------------------------
	# Draw the box rectangle from box Rect x1,y1,x2,y2
	#--------------------------------------------------------------------
	def drawBoxesOnPdf (self, pdfFilename, boxes, WIDTH=1, COLORBOX=(0,0,1), COLORTEXT=(1,0,1)):
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
			print (f"+++ rect '{rect}'")
			page.draw_rect (rect, color=COLORBOX, width=WIDTH)  # Red border
			page.insert_text ((box[0]+5, box[1]+15), text, fontsize=16, color=COLORTEXT)  # Blue text

		# Save the modified PDF
		pdf_document.save(output_pdf)
		pdf_document.close()
		return output_pdf

	#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()
