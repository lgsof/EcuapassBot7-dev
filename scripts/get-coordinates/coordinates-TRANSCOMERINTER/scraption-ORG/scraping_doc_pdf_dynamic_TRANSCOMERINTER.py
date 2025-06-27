#!/usr/bin/env python3

import fitz  # Form PyMuPDF. Added to pyinstaller hidden modules
from scraping_doc_pdf_dynamic import ScrapingDocPdf_Dynamic

#--------------------------------------------------------------------
# Set document text boxes from ALL detected PDF's boxes
#--------------------------------------------------------------------
def main ():
	import os
	#pdfFile = "CPI-TRANSCOMERINTER-TEST-0010000000082.pdf"
	#pdf     = ScrapingDocPdfDynamic_TRANSCOMERINTER_Cartaporte (pdfFile, "TRANSCOMERINTER", "ECUADOR", "TULCAN", None, os.getcwd () )

	pdfFile = "MCI-TRANSCOMERINTER-TEST-1.pdf"
	pdf     = ScrapingDocPdfDynamic_TRANSCOMERINTER_Manifiesto (pdfFile, "TRANSCOMERINTER", "ECUADOR", "TULCAN", None, os.getcwd () )

	fullTest (pdf, pdfFile)

def simpleTest (pdf, pdfFile):
	pdf.getPdfCoordinates (pdfFile)

def fullTest (pdf, pdfFile):
	pdf.getPdfCoordinates (pdfFile)
	boxes  = pdf.getRawBoxesFromPdf (pdfFile)
	outPdf = pdf.drawBoxesOnPdf (pdfFile, boxes [:69], WIDTH=3, COLORBOX=(1,0,0), COLORTEXT=(1,0.5,0.5))

	textBoxes = pdf.getDocumentBoxesFromPdf (boxes)
	pdf.printBoxes (textBoxes, "TextBoxes")
	pdf.drawBoxesOnPdf (outPdf, textBoxes, COLORBOX=(0,0,1), COLORTEXT=(0,0,1))

#--------------------------------------------------------------------
# Base class
#--------------------------------------------------------------------
class ScrapingDocPdfDynamic_TRANSCOMERINTER (ScrapingDocPdf_Dynamic):
	def __init__ (self, pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		super().__init__ (pdfFilepath, empresa, pais, distrito, credentials, runningDir)

	#--------------------------------------------------------------------
	# Return TRANSCOMERINTER CLASS for Cartaporte or Manifiesto
	#--------------------------------------------------------------------
	def getScrapingDocPdfCLASS_Cartaporte (self):
		return ScrapingDocPdfDynamic_TRANSCOMERINTER_Cartaporte

	def getScrapingDocPdfCLASS_Manifiesto (self):
		return ScrapingDocPdfDynamic_TRANSCOMERINTER_Manifiesto

	#--------------------------------------------------------------------
	# Get raw (all detected) boxes from PDF file
	#--------------------------------------------------------------------
	def getRawBoxesFromPdf (self, pdf_path):
		def equals (a, b):
			return abs (a-b) < 2

		def getValidLines (lines):
			validLines = []
			while True:
				line = lines.pop (i)
				for k in ['x1','x2','y1','y2']:
					if any ([equals (line[k], l[k]) for l in lines]):
						validLines.append (lines [i])
				if len (lines) == 0:
					break
			return validLines

		#----------- From box lines get box coords-----------------------
		def getBoxFromLines (lines):
			x1 = min ([l ['x1'] for l in lines])
			x2 = max ([l ['x2'] for l in lines])
			y1 = min ([l ['y1'] for l in lines])
			y2 = max ([l ['y2'] for l in lines])
			boxCoords = fitz.Rect (x1, y1, x2, y2)
			print (f"+++ boxCoords: '{boxCoords}'")
			return boxCoords
		#----------------------------------------------------------------
		doc  = fitz.open(pdf_path)
		page = doc[0]
		shapes = page.get_drawings() # Retrieve all drawing commands

		boxes, lines, nBox = [], [], 0
		for k, shape in enumerate (shapes):
			for i, item in enumerate (shape["items"]):
				if item[0] == "re":	# Check if the item is a line
					coords = {'x1':item [1][0],'y1':item [1][1],'x2':item [1][2],'y2':item [1][3]}
					lines.append (coords)

			if len (lines) == 4:
				print (f"\n>>> Box: '{nBox}'")
				print (f">>> Lines: '{lines}'")
				nBox += 1
				validLines = getValidLines (lines)
				boxes.append (getBoxFromLines (validLines))
				lines = []

		return boxes

	#--------------------------------------------------------------------
	#-- Overwritten box functions
	#--------------------------------------------------------------------
	def boxMercancia (self, boxTop, boxBottom):
		box = (boxTop [0], boxTop [3], boxTop [2], boxBottom [3])
		return (box)

	def boxLabel (self, box, nLines=1):
		offset = 11*nLines
		return (box [0], box [1] + offset , box [2], box [3])

#--------------------------------------------------------------------
# Scraping class for Manifiesto
#--------------------------------------------------------------------
class ScrapingDocPdfDynamic_TRANSCOMERINTER_Manifiesto (ScrapingDocPdfDynamic_TRANSCOMERINTER):
	def __init__ (self, pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		super().__init__ (pdfFilepath, empresa, pais, distrito, credentials, runningDir)

	#--------------------------------------------------------------------
	# Get document boxes (containing document text) from PDF file
	#--------------------------------------------------------------------
	def getDocumentBoxesFromPdf (self, boxes):
		textBoxes = {}
		textBoxes ["txt0b"]     = self.boxLabel (boxes [5])    # Permiso
		textBoxes ["txt0a"]     = self.boxLabel (boxes [29])   # Pais
		textBoxes ["txt00"]     = self.boxSimple (boxes [2])   # Numero
		textBoxes ["txt01"]     = self.boxLabel (boxes [3])
		textBoxes ["txt02"]     = self.boxLabel (boxes [4])
		textBoxes ["txt03"]     = self.boxLabel (boxes [5])

		# Camion o Tracto Camion:
		textBoxes ["txt04"]     = self.boxLabel (boxes [7])
		textBoxes ["txt05"]     = self.boxLabel (boxes [8])
		textBoxes ["txt06"]     = self.boxLabel (boxes [9])
		textBoxes ["txt07"]     = self.boxLabel (boxes [10])
		textBoxes ["txt08"]     = self.boxLabel (boxes [11])

		# Unidad Carga:
		textBoxes ["txt09"]     = self.boxLabel (boxes [13])
		textBoxes ["txt10"]     = self.boxLabel (boxes [14])
		textBoxes ["txt11"]     = self.boxLabel (boxes [15])
		textBoxes ["txt12"]     = self.boxLabel (boxes [16])

		# Conductor
		textBoxes ["txt13"]     = self.boxLabel (boxes [18])
		textBoxes ["txt14"]     = self.boxLabel (boxes [20])
		textBoxes ["txt15"]     = self.boxLabel (boxes [21])
		textBoxes ["txt16"]     = self.boxLabel (boxes [24])
		textBoxes ["txt17"]     = self.boxLabel (boxes [25])
		# Auxiliar
		textBoxes ["txt18"]     = self.boxLabel (boxes [19])
		textBoxes ["txt19"]     = self.boxLabel (boxes [22])
		textBoxes ["txt20"]     = self.boxLabel (boxes [23])
		textBoxes ["txt21"]     = self.boxLabel (boxes [26])
		textBoxes ["txt22"]     = self.boxLabel (boxes [27])

		# Carga
		textBoxes ["txt23"]     = self.boxLabel (boxes [29])
		textBoxes ["txt24"]     = self.boxLabel (boxes [30])

		# Tipo de Carga
		textBoxes ["txt25_0"]   = self.boxSimple (boxes [32])
		textBoxes ["txt25_1"]   = self.boxSimple (boxes [32])
		textBoxes ["txt25_2"]   = self.boxSimple (boxes [32])
		textBoxes ["txt25_3"]   = self.boxSimple (boxes [32])
		textBoxes ["txt25_4"]   = self.boxSimple (boxes [32])
		textBoxes ["txt25_5"]   = self.boxTipoCarga (boxes [32],boxes [32])

		textBoxes ["txt26"]     = self.boxLabel (boxes [33])
		textBoxes ["txt27"]     = self.boxLabel (boxes [34])

		textBoxes, nBox = self.getTextBoxesMercancia (textBoxes, boxes, startingBox=43)
		# Mercancia
#		textBoxes ["txt28"]     = self.boxMercancia (boxes [38],boxes [46])
#		textBoxes ["txt29"]     = self.boxMercancia (boxes [39],boxes [46])
#		textBoxes ["txt30"]     = self.boxMercancia (boxes [40],boxes [46])
#		textBoxes ["txt31"]     = self.boxMercancia (boxes [41],boxes [47])
#		textBoxes ["txt32_1"]   = self.boxMercancia (boxes [44],boxes [48])
#		textBoxes ["txt32_2"]   = self.boxSimple (boxes [48])
#		textBoxes ["txt32_3"]   = self.boxMercancia (boxes [45],boxes [49])
#		textBoxes ["txt32_4"]   = self.boxSimple (boxes [49])
#		textBoxes ["txt33_1"]   = self.boxMercancia (boxes [43],boxes [50])
#		textBoxes ["txt33_2"]   = self.boxSimple (boxes [50])

#		# Incoterm
		textBoxes ["txt34"]     = self.boxLabel (boxes [nBox]); nBox += 2

		# Totals
		textBoxes ["txt32_2"]   = self.boxSimple (boxes [nBox]); nBox += 1  # Total Peso Neto
		textBoxes ["txt32_4"]   = self.boxSimple (boxes [nBox]); nBox += 1    # Total Peso Bruto
		textBoxes ["txt33_2"]   = self.boxSimple (boxes [nBox]); nBox += 1    # Total Volumen

		# Observaciones y Aduanas
		textBoxes ["txt35"]     = self.boxLabel (boxes [nBox]); nBox += 1
		textBoxes ["txt37"]     = self.boxLabel (boxes [nBox]); nBox += 1
		textBoxes ["txt38"]     = self.boxLabel (boxes [nBox]); nBox += 1

		# Firma, Fecha Emision
		textBoxes ["txt36"]     = self.boxLabel (boxes [nBox]); nBox += 1
		textBoxes ["txt39"]     = self.boxSimple (boxes [nBox]); nBox += 1
		textBoxes ["txt40"]     = self.boxLabel (boxes [nBox]); nBox += 1

		return textBoxes

	#----------------------------------------------------------------------------
	# Get boxes for diynamic mercancia table: detailes rows and final description
	#----------------------------------------------------------------------------
	def getTextBoxesMercancia (self, textBoxes, boxes, startingBox):
		#----------- width --------------
		def boxWidth (box):
			return box [2] - box [0]
		#--------------------------------
		# Set a mercancia dict {'txtXX':item,....}
		cpis, dscs, cnts, clss, pnts, pbts, vols, gDesc = [], [], [], [], [], [], [], None
		mercanciaDic = {"28":cpis, "29":dscs, "30":cnts, "31":clss, "32_1":pnts, "32_3":pbts, "33_1":vols}
		mercanciaDic = {"txt"+x:item  for x, item in mercanciaDic.items ()}

		nb = startingBox
		# Add boxes to each mercancia's item
		while (True):
			for item in mercanciaDic.values ():
				item.append (boxes [nb]); nb += 1

			if boxWidth (boxes [nb]) > 300: 
				gDesc = boxes [nb]; nb+=1
				break

		# Set textBoxes' coordinates from item boxes coordinates
		first, last = 0, len (cpis) - 1
		for txtKey, item in mercanciaDic.items ():
			textBoxes [txtKey] = (item [first][0], item [first][1], item[first][2], item [last][3])

		# Set TRANSCOMERINTER's general description item
		textBoxes ['appBodega'] = gDesc

		return textBoxes, nb

#--------------------------------------------------------------------
# Scraping class for Cartaporte
#--------------------------------------------------------------------
class ScrapingDocPdfDynamic_TRANSCOMERINTER_Cartaporte (ScrapingDocPdfDynamic_TRANSCOMERINTER):
	def __init__ (self, pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		super().__init__ (pdfFilepath, empresa, pais, distrito, credentials, runningDir)

	#--------------------------------------------------------------------
	# Get document boxes (containing document text) from PDF file
	#--------------------------------------------------------------------
	def getDocumentBoxesFromPdf (self, boxes):
		textBoxes = {}
		textBoxes ["txt0b"]     = self.boxLabel (boxes [3])   # Permiso
		textBoxes ["txt0a"]     = self.boxLabel (boxes [5])   # Pais
		textBoxes ["txt00"]     = self.boxSimple (boxes [2])   # Numero
		textBoxes ["txt01"]     = self.boxLabel (boxes [3])
		textBoxes ["txt02"]     = self.boxLabel (boxes [6])
		textBoxes ["txt03"]     = self.boxLabel (boxes [8])
		textBoxes ["txt04"]     = self.boxLabel (boxes [10])
		textBoxes ["txt05"]     = self.boxLabel (boxes [4])
		textBoxes ["txt06"]     = self.boxLabel (boxes [5])
		textBoxes ["txt07"]     = self.boxLabel (boxes [7])
		textBoxes ["txt08"]     = self.boxLabel (boxes [9])
		textBoxes ["txt09"]     = self.boxLabel (boxes [11])

		textBoxes ["txt10"]     = self.boxMercancia (boxes [12], boxes [16])
		textBoxes ["txt11"]     = self.boxMercancia (boxes [13], boxes [16])
		textBoxes ["txt12"]     = self.boxMercancia (boxes [14], boxes [16])

		textBoxes ["txt13_1"]   = self.boxLabel (boxes [17])
		textBoxes ["txt13_2"]   = self.boxLabel (boxes [18])
		textBoxes ["txt14"]     = self.boxLabel (boxes [19])
		textBoxes ["txt15"]     = self.boxLabel (boxes [20])
		textBoxes ["txt16"]     = self.boxLabel (boxes [21])
		textBoxes ["txt17_11"]  = self.boxSimple (boxes [28])
		textBoxes ["txt17_12"]  = self.boxSimple (boxes [29])
		textBoxes ["txt17_13"]  = self.boxSimple (boxes [30])
		textBoxes ["txt17_14"]  = self.boxSimple (boxes [31])

		textBoxes ["txt17_21"]  = self.boxSimple (boxes [33])
		textBoxes ["txt17_22"]  = self.boxSimple (boxes [34])
		textBoxes ["txt17_23"]  = self.boxSimple (boxes [35])
		textBoxes ["txt17_24"]  = self.boxSimple (boxes [36])
		
		textBoxes ["txt17_31"]  = self.boxSimple (boxes [38])
		textBoxes ["txt17_32"]  = self.boxSimple (boxes [39])
		textBoxes ["txt17_33"]  = self.boxSimple (boxes [40])
		textBoxes ["txt17_34"]  = self.boxSimple (boxes [41])

		textBoxes ["txt17_41"]  = self.boxSimple (boxes [43])
		textBoxes ["txt17_42"]  = self.boxSimple (boxes [44])
		textBoxes ["txt17_43"]  = self.boxSimple (boxes [45])
		textBoxes ["txt17_44"]  = self.boxSimple (boxes [46])

		textBoxes ["txt18"]     = self.boxLabel (boxes [50])
		textBoxes ["txt19"]     = self.boxLabel (boxes [52])
		textBoxes ["txt20"]     = self.boxLabel (boxes [53])
		textBoxes ["txt21"]     = self.boxLabel (boxes [48])
		textBoxes ["txt22"]     = self.boxLabel (boxes [49])
		textBoxes ["txt23"]     = self.boxLabel (boxes [51])

		return textBoxes

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()
