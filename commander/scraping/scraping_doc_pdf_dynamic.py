#!/usr/bin/env python3
"""
Detect Horizontal and Vertical Lines
Extract the lines using pdfplumber and classify them:
"""

import os, sys, json
import fitz  # Form PyMuPDF. Added to pyinstaller hidden modules

from info.ecuapass_utils import Utils
from info.ecuapass_exceptions import EcudocPdfCoordinatesError

from .scraping_doc_pdf import ScrapingDocPdf


#--------------------------------------------------------------------
# Class for extracting 'dynamically' coordinates from a PDF 
#--------------------------------------------------------------------
class ScrapingDocPdf_Dynamic (ScrapingDocPdf):
	def __init__ (self, pdfFilepath, empresa, pais, distrito):
		self.cartaporteCLASS = None
		self.manifiestoCLASS = None
		super().__init__ (pdfFilepath, empresa, pais, distrito)

	#--------------------------------------------------------------------
	# Get from PDF coordinates where text is written (no labels)
	#--------------------------------------------------------------------
	def getPdfCoordinates (self, docType, pdfFilepath):
		coords = None
		try:
			if docType == 'CARTAPORTE':
				scrapingCLASS = self.getScrapingDocPdfCLASS_Cartaporte ()    # Instanced in subclasses
			elif docType == 'MANIFIESTO':
				scrapingCLASS = self.getScrapingDocPdfCLASS_Manifiesto ()    # Instances in subclasses
			else:
				raise Exception ("ERROR::Tipo de documento no encontrado desde archivo : '{os.path.basename (pdfFilepath)}'")

			scrapingDocPdf = scrapingCLASS (self.pdfFilepath, self.empresa, self.pais, self.distrito)

			rawBoxes       = scrapingDocPdf.getRawBoxesFromPdf (pdfFilepath)    # Specific for each subclass
			docBoxes       = scrapingDocPdf.getDocumentBoxesFromPdf (rawBoxes)  # Specific for each subclass
			coords         = scrapingDocPdf.convertBoxesToCoords (docBoxes)     # General in base class

			jsonFilename   = pdfFilepath.split (".")[0] + "-COORDS.json"
			json.dump (coords, open (jsonFilename, "w"), indent=4)

		except Exception as e:
			raise EcudocPdfCoordinatesError ('PDFERROR::Problemas extrayendo coordenadas desde el PDF') from e

		return coords

	#--------------------------------------------------------------------
	# Get raw (all detected) boxes from PDF file
	# Default: Detect boxes in PDF (SanchezPolo)
	# Override: Detect lines in PDF (Transcomerinter)
	#--------------------------------------------------------------------
	def getRawBoxesFromPdf (self, pdf_path):
		#doc = fitz.open(pdf_path)
		#page = doc[0]

		# Retrieve all drawing commands
		shapes = self.pdfPage.get_drawings()

		boxes = []
		for k, shape in enumerate (shapes):
			for i, item in enumerate (shape["items"]):
				#print (f">>> k: {k}: ", item)
				if item[0] == "re":	# Check if the item is a line
					boxes.append (item [1])
		return boxes

	#--------------------------------------------------------------------
	# Convert boxes (Rect type) to coords: x, y, width, height
	#--------------------------------------------------------------------
	def convertBoxesToCoords (self, docBoxes):
		def getCoordFromBox (box):
			return tuple ([int (x) for x in [box[0],box[1],box[2]-box[0]+1,box[3]-box[1]+1]])

		docCoords = {}
		for txtKey, item in docBoxes.items ():
			if item and type (item) is not list:
				docCoords [txtKey] = getCoordFromBox (item)
			elif item:
				coordsList = []
				for box in item:
					coordsList.append (getCoordFromBox (box))

				docCoords [txtKey] = coordsList

		return docCoords

	#--------------------------------------------------------------------
	# Get box region containing the specific type of document text
	#--------------------------------------------------------------------

	def boxSimple (self, box):
		return (box)

	def boxLabel (self, box, nLines=1):
		offset = 9*nLines          # For SanchezPolo, different for Transcomerinter
		return (box [0], box [1] + offset , box [2], box [3])

	def boxMercancia (self, boxTop, boxBottom):
		box = (boxTop [0], boxTop [3], boxTop [2], boxBottom [1]-30)
		return (box)

	def boxIncoterms (self, boxTop1, boxTop2, boxBottom):
		box = (boxTop1 [0], boxTop1 [3] + 18, boxTop2 [2], boxBottom [1])
		return (box)

	def boxGastos (self, boxTop, rowNumber):
		rowSize = 24 if rowNumber !=3 else 14
		rowPos  = boxTop[3] + rowNumber * 24
		box = (boxTop [0], rowPos , boxTop [2], rowPos + rowSize)
		return (box)

	def boxMRN (self, left, right, bottom):
		box = (left [0], bottom [1]-30, right [2], bottom [1]) 
		return box

	def boxTipoCarga (self, top, bottom):
		offset = (top [2]-top[0]) / 4
		box = top [2]-offset, top [3], top [2], bottom [1]
		return box

	def boxEmpty (self, box):
		offset = 9          # For SanchezPolo, different for Transcomerinter
		return (box [0], box [1] + offset , box [2], box [3])

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
	def printBoxes (self, boxes, title='Boxes'):
		print (f"\n+++ {title}:")
		for i, b in enumerate (boxes):
			print (f"\t>>> {i}:", f"'{b}' : '{boxes [b]}'" if type (boxes) is dict else b )

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
			if not box:
				continue
			elif type (box) is list:
				box = box [0]

			text = str (k).zfill(2)
			rect = fitz.Rect (box)  # (x0, y0, x1, y1)
			page.draw_rect (rect, color=COLORBOX, width=WIDTH)  # Red border
			centerX = box [0] + (box[2]-box[0])/2
			centerY = 5 + box [1] + (box[3]-box[1])/2
			page.insert_text ((centerX, centerY), text, fontsize=16, color=COLORTEXT)  # Blue text
			#page.insert_text ((box[2]-55, box[3]-5), text, fontsize=16, color=COLORTEXT)  # Blue text

		# Save the modified PDF
		pdf_document.save(output_pdf)
		pdf_document.close()
		return output_pdf

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()
