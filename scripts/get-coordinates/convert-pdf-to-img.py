#!/usr/bin/env python3
import pdfplumber
import sys, json
import subprocess 

"""
Extracts text from a file of coordinates and the image of a PDF
Then, creates a JSON file of coordinates
"""
USAGE="""
extract-coordinates-pdf.py [--getImg|--pdfSize] <Coordinates file>
"""

def main ():
	args = sys.argv 
	if len (args) < 2:
		print (USAGE)
		sys.exit (0)

	option = args [1]
	if option == "--pdfSize":
		pdfFilename = args [2]
		getPdfSize
	elif option == "--getImg":
		pdfFilename = args [2]
		convertPdfToPng (pdfFilename)
	else:
		print ("Opción no reconocida")


def getPdfSize (pdfFilename):
	with pdfplumber.open(pdfFilename) as pdf:
		page = pdf.pages [0]
		width  = page.width
		height = page.height
		print(f"{width}, {height}")

	return width, height

def convertPdfToPng (pdfFilepath):
	width, height = getPdfSize (pdfFilepath)
	outFile = pdfFilepath.split (".")[0] + f"-{width}x{height}" + ".png"
	cmm = ["convert", "-density", "150", pdfFilepath, "-resize", f"{width}x{height}", outFile]
	print (f"Convert command: ", cmm)
	subprocess.run (cmm)

#--------------------------------------------------------------------
#--------------------------------------------------------------------
main ()


