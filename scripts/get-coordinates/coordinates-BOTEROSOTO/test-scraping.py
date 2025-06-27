#!/usr/bin/env python3
import os, sys
import fitz  # Form PyMuPDF. Added to pyinstaller hidden modules
from scraping.scraping_doc_pdf_dynamic_BOTEROSOTO import ScrapingDocPdfDynamic_BOTEROSOTO

#--------------------------------------------------------------------
# Set document text boxes from ALL detected PDF's boxes
#--------------------------------------------------------------------
def main ():
	#pdfFile = "CPIC-BOTEROSOTO-TEST-0060000000913.pdf"
	pdfFile = "TEST-CPI-BOTERO-ADIQUIM.pdf"
	#pdfFile = sys.argv [1]
#	if "CPI" in pdfFile:
#		pdfClass = ScrapingDocPdfDynamic_BOTEROSOTO_Cartaporte
#	elif "MCI" in pdfFile: 
#		pdfClass = ScrapingDocPdfDynamic_BOTEROSOTO_Manifiesto
#	else:
#		pdfClass = ScrapingDocPdfDynamic_BOTEROSOTO 
	pdfClass = ScrapingDocPdfDynamic_BOTEROSOTO 

	# Create an instance
	pdf = pdfClass (pdfFile, "BOTEROSOTO", "ECUADOR", "TULCAN")

	fullTest (pdf, pdfFile)

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def fullTest (pdf, pdfFile):
	boxes     = pdf.getRawBoxesFromPdf_TCI (pdfFile)
	outPdf    = pdf.drawBoxesOnPdf (pdfFile, boxes, WIDTH=3, COLORBOX=(1,0,0), COLORTEXT=(1,0.5,0.5))
#	textBoxes = pdf.getDocumentBoxesFromPdf (boxes)
#	pdf.printBoxes (textBoxes, "TextBoxes")
#	pdf.drawBoxesOnPdf (outPdf, textBoxes, COLORBOX=(0,0,1), COLORTEXT=(0,0,1))

#--------------------------------------------------------------------
#--------------------------------------------------------------------
main ()
