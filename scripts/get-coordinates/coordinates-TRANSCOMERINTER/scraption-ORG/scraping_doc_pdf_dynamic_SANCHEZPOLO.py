#!/usr/bin/env python3

from scraping_doc_pdf_dynamic import ScrapingDocPdf_Dynamic


#--------------------------------------------------------------------
# Set document text boxes from ALL detected PDF's boxes
#--------------------------------------------------------------------
def main ():
	import os
	pdfFile = "CPI-SANCHEZPOLO-TEST-061984-24.pdf"
	pdf     = ScrapingDocPdfDynamic_SANCHEZPOLO_Cartaporte (pdfFile, "SANCHEZPOLO", "ECUADOR", "TULCAN", None, os.getcwd () )

	#pdfFile = "MCI-TRANSCOMERINTER-TEST-1.pdf"
	#pdf     = ScrapingDocPdfDynamic_TRANSCOMERINTER_Manifiesto (pdfFile, "TRANSCOMERINTER", "ECUADOR", "TULCAN", None, os.getcwd () )

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
# Class for extracting 'dynamically' coordinates from a PDF 
#--------------------------------------------------------------------
class ScrapingDocPdfDynamic_SANCHEZPOLO (ScrapingDocPdf_Dynamic):
	def __init__ (self, pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		super().__init__ (pdfFilepath, empresa, pais, distrito, credentials, runningDir)

	#--------------------------------------------------------------------
	# Return TRANSCOMERINTER CLASS for Cartaporte or Manifiesto
	#--------------------------------------------------------------------
	def getScrapingDocPdfCLASS_Cartaporte (self):
		return ScrapingDocPdfDynamic_SANCHEZPOLO_Cartaporte

	def getScrapingDocPdfCLASS_Manifiesto (self):
		return ScrapingDocPdfDynamic_SANCHEZPOLO_Manifiesto

#--------------------------------------------------------------------
# Scraping class for Manifiesto
#--------------------------------------------------------------------
class ScrapingDocPdfDynamic_SANCHEZPOLO_Manifiesto (ScrapingDocPdfDynamic_SANCHEZPOLO):
	def __init__ (self, pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		super().__init__ (pdfFilepath, empresa, pais, distrito, credentials, runningDir)

	#--------------------------------------------------------------------
	# Get document boxes (containing document text) from PDF file
	#--------------------------------------------------------------------
	def getDocumentBoxesFromPdf (self, boxes):
		b = boxes
		textBoxes = {}
		textBoxes ["txt0b"]     = self.boxLabel (b[5])
		textBoxes ["txt0a"]     = self.boxLabel (b[33])
		textBoxes ["txt00"]     = self.boxSimple (b[1])
		textBoxes ["txt01"]     = self.boxLabel (b[4])
		textBoxes ["txt02"]     = self.boxLabel (b[5])
		textBoxes ["txt03"]     = self.boxLabel (b[6])

		# Camion o Tracto Camion:
		textBoxes ["txt04"]     = self.boxLabel (b[9])
		textBoxes ["txt05"]     = self.boxLabel (b[10])
		textBoxes ["txt06"]     = self.boxLabel (b[11])
		textBoxes ["txt07"]     = self.boxLabel (b[12])
		textBoxes ["txt08"]     = self.boxLabel (b[13])

		# Unidad Carga:
		textBoxes ["txt09"]     = self.boxLabel (b[16])
		textBoxes ["txt10"]     = self.boxLabel (b[17])
		textBoxes ["txt11"]     = self.boxLabel (b[18])
		textBoxes ["txt12"]     = self.boxLabel (b[19])
		textBoxes ["txt13"]     = self.boxLabel (b[22])

		textBoxes ["txt14"]     = self.boxLabel (b[24])
		textBoxes ["txt15"]     = self.boxLabel (b[25])
		textBoxes ["txt16"]     = self.boxLabel (b[28])
		textBoxes ["txt17"]     = self.boxLabel (b[29])
		textBoxes ["txt18"]     = self.boxLabel (b[23])
		textBoxes ["txt19"]     = self.boxLabel (b[26])
		textBoxes ["txt20"]     = self.boxLabel (b[27])
		textBoxes ["txt21"]     = self.boxLabel (b[30])
		textBoxes ["txt22"]     = self.boxLabel (b[31])
		textBoxes ["txt23"]     = self.boxLabel (b[33])
		textBoxes ["txt24"]     = self.boxLabel (b[34])
		textBoxes ["txt25_0"]   = self.boxEmpty (b[38])
		textBoxes ["txt25_1"]   = self.boxSimple (b[56])
		textBoxes ["txt25_2"]   = self.boxSimple (b[58])
		textBoxes ["txt25_3"]   = self.boxSimple (b[60])
		textBoxes ["txt25_4"]   = self.boxSimple (b[62])
		textBoxes ["txt25_5"]   = self.boxTipoCarga (b[34],b[37])
		textBoxes ["txt26"]     = self.boxLabel (b[36])
		textBoxes ["txt27"]     = self.boxLabel (b[37])
		textBoxes ["txt28"]     = self.boxMercancia (b[38],b[46])
		textBoxes ["txt29"]     = self.boxMercancia (b[39],b[46])
		textBoxes ["txt30"]     = self.boxMercancia (b[40],b[46])
		textBoxes ["txt31"]     = self.boxMercancia (b[41],b[47])
		textBoxes ["txt32_1"]   = self.boxMercancia (b[44],b[48])
		textBoxes ["txt32_2"]   = self.boxSimple (b[48])
		textBoxes ["txt32_3"]   = self.boxMercancia (b[45],b[49])
		textBoxes ["txt32_4"]   = self.boxSimple (b[49])
		textBoxes ["txt33_1"]   = self.boxMercancia (b[43],b[50])
		textBoxes ["txt33_2"]   = self.boxSimple (b[50])

		# Incoterm
		textBoxes ["txt34"]     = self.boxLabel (b[46], nLines=0)

		textBoxes ["txt35"]     = self.boxLabel (b[51])
		textBoxes ["txt36"]     = self.boxLabel (b[54])
		textBoxes ["txt37"]     = self.boxLabel (b[52])
		textBoxes ["txt38"]     = self.boxLabel (b[53])
		textBoxes ["txt39"]     = self.boxEmpty (b[38])
		textBoxes ["txt40"]     = self.boxLabel (b[55])

		# Special fields
		textBoxes ["appMRN"]    = self.boxMRN (b[46], b[40], b[46])
		return textBoxes

#--------------------------------------------------------------------
# Scraping class for Cartaporte
#--------------------------------------------------------------------
class ScrapingDocPdfDynamic_SANCHEZPOLO_Cartaporte (ScrapingDocPdfDynamic_SANCHEZPOLO):
	def __init__ (self, pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		super().__init__ (pdfFilepath, empresa, pais, distrito, credentials, runningDir)

	#--------------------------------------------------------------------
	# Get document boxes (containing document text) from PDF file
	#--------------------------------------------------------------------
	def getDocumentBoxesFromPdf (self, boxes):
		b = boxes
		textBoxes = {}
		textBoxes ["txt0b"]     = self.boxSimple (b[1])
		textBoxes ["txt0a"]     = self.boxSimple (b[1])
		textBoxes ["txt00"]     = self.boxSimple (b[1])
		textBoxes ["txt01"]     = self.boxLabel (b[2])
		textBoxes ["txt02"]     = self.boxLabel (b[4])
		textBoxes ["txt03"]     = self.boxLabel (b[7])
		textBoxes ["txt04"]     = self.boxLabel (b[10])
		textBoxes ["txt05"]     = self.boxLabel (b[3])
		textBoxes ["txt06"]     = self.boxLabel (b[5])
		textBoxes ["txt07"]     = self.boxLabel (b[6])
		textBoxes ["txt08"]     = self.boxLabel (b[8])
		textBoxes ["txt09"]     = self.boxLabel (b[9])
		textBoxes ["txt10"]     = self.boxMercancia (b[11], b[19])
		textBoxes ["txt11"]     = self.boxMercancia (b[12], b[19])
		textBoxes ["txt12"]     = self.boxMercancia (b[13], b[19])
		textBoxes ["txt13_1"]   = self.boxLabel (b[15])
		textBoxes ["txt13_2"]   = self.boxLabel (b[16])
		textBoxes ["txt14"]     = self.boxLabel (b[17], 2)
		textBoxes ["txt15"]     = self.boxLabel (b[18], 2)
		textBoxes ["txt16"]     = self.boxIncoterms (b[17], b[18], b[20])
		textBoxes ["txt17_11"]  = self.boxGastos (b[22], 0)
		textBoxes ["txt17_12"]  = self.boxGastos (b[22], 1)
		textBoxes ["txt17_13"]  = self.boxGastos (b[22], 2)
		textBoxes ["txt17_14"]  = self.boxGastos (b[22], 3)

		textBoxes ["txt17_21"]  = self.boxGastos (b[23], 0)
		textBoxes ["txt17_22"]  = self.boxGastos (b[23], 1)
		textBoxes ["txt17_23"]  = self.boxGastos (b[23], 2)
		textBoxes ["txt17_24"]  = self.boxGastos (b[23], 3)
		
		textBoxes ["txt17_31"]  = self.boxGastos (b[24], 0)
		textBoxes ["txt17_32"]  = self.boxGastos (b[24], 1)
		textBoxes ["txt17_33"]  = self.boxGastos (b[24], 2)
		textBoxes ["txt17_34"]  = self.boxGastos (b[24], 3)

		textBoxes ["txt17_41"]  = self.boxGastos (b[25], 0)
		textBoxes ["txt17_42"]  = self.boxGastos (b[25], 1)
		textBoxes ["txt17_43"]  = self.boxGastos (b[25], 2)
		textBoxes ["txt17_44"]  = self.boxGastos (b[25], 3)

		textBoxes ["txt18"]     = self.boxLabel (b[27])
		textBoxes ["txt19"]     = self.boxLabel (b[29])
		textBoxes ["txt20"]     = self.boxLabel (b[30])
		textBoxes ["txt21"]     = self.boxLabel (b[20])
		textBoxes ["txt22"]     = self.boxSimple (b[28])
		textBoxes ["appMRN"]    = self.boxMRN (b[11], b[12], b[19])

		return textBoxes

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()
