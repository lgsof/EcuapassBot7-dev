#!/usr/bin/env python3
import sys, json, subprocess 
#import pdfplumber
import re

USAGE="""
Different utils for extracting text from PDF files\n
pdf-coordinates.py <Option> [param1] [param2]
Options: 
	--pdfSize
	--pdfToImg <Pdf file>
	--txtToJson <Coordinates text file>
	--pdfBoxes <Pdf file> <Coordinates file>
"""

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def main ():
	args = sys.argv 
	if len (args) < 2:
		print (USAGE)
		sys.exit (0)

	option = args [1]
	pdfFilename = args [2]
	if option == "--pdfSize":
		getPdfSize (pdfFilename)
	elif option == "--pdfToImg":
		convertPdfToImg (pdfFilename)
	elif option == "--txtToJson":
		txtCoordsFile = args [2]
		convertLineCoordsToJson (txtCoordsFile)
	elif option == "--pdfBoxes":
		txtCoordsFile = args [2]
		extractTextFromPdfBoxes (pdfFilename, txtCoordsFile)

#--------------------------------------------------------------------
# Extract text from given boxes coordinates
#--------------------------------------------------------------------
def extractTextFromPdfBoxes (pdfFilename, txtCoordsFile):
	jsonCoordsFile = convertLineCoordsToJson (txtCoordsFile)
	createDocumentCoords (jsonCoordsFile)

	coordinates = open (txtCoordsFile).readlines()
	boxesDic = {}
	for line in coordinates:
		id         = line.split (":")[0]
		valuesList = line.split (":")[1].split(",")
		values     = [int (x.strip()) for x in valuesList]
		boxesDic [id] = values

	appFields = extract_text_from_boxes (pdfFilename, boxesDic)

	# Print the extracted data
	for id, text in appFields.items():
		print(f"  {id}: {text}")


#--------------------------------------------------------------------
#--------------------------------------------------------------------
def extract_text_from_boxes (pdfFilename, boxesDic):
	import pdfplumber
	appFields = {}
	with pdfplumber.open(pdfFilename) as pdf:
		page = pdf.pages [0]
		print(f"{page.width}, {page.height}")
		for k, box in boxesDic.items ():
			x0, y0, x1, y1 = box[0], box[1], box[0]+box[2], box[1]+box[3]  # Coordinates of the box
			cropped_page = page.within_bbox((x0, y0, x1, y1))
			text = cropped_page.extract_text() if cropped_page else ""
			appFields [k] = text.strip() if text else ""
	return appFields

def convertLineCoordsToJson (txtCoordsFile):
	#------ "0c:224 × 25 @ (171, 30)" ----------------------
	templates = {"pixspy":r'(\d+)c:(\d+) × (\d+) @ \((\d+), (\d+)\)', 
			     "kpaint": r'(\d+),(\d+),(\d+),(\d+),(\d+)'
	}
	def getNumbers (text, pattern="pixspy"):
		match   = re.match (pattern, text)
		numbers = match.groups ()
		return numbers
	#------------------------------------------------------

	coordinates = open (txtCoordsFile).readlines()
	boxesDic = {}
	for line in coordinates:
		id         = "txt" + line.split (":")[0]
		values     = getNumbers (text, "pixspy")
		boxesDic [id] = values

	jsonCoordsFile = txtCoordsFile.split (".")[0] + ".json"
	json.dump (boxesDic, open (jsonCoordsFile, "w"), indent=4)
	return jsonCoordsFile

def convertLineCoordsToJson_kpaint (txtCoordsFile):
	coordinates = open (txtCoordsFile).readlines()
	boxesDic = {}
	for line in coordinates:
		id         = "txt" + line.split (":")[0]
		valuesList = line.split (":")[1].split(",")
		values     = [int (x.strip()) for x in valuesList]
		boxesDic [id] = values

	jsonCoordsFile = txtCoordsFile.split (".")[0] + ".json"
	json.dump (boxesDic, open (jsonCoordsFile, "w"), indent=4)
	return jsonCoordsFile


def createDocumentCoords (jsonCoordsFile):
	if "Cartaporte" in jsonCoordsFile:
		cpiCoords = json.load (open (jsonCoordsFile))
		mciFile   = jsonCoordsFile.replace ("Cartaporte", "Manifiesto")
		mciCoords = json.load (open (mciFile))
		docFile   = mciFile.replace ("-Manifiesto","")
	elif "Manifiesto" in jsonCoordsFile:
		mciCoords = json.load (open (jsonCoordsFile))
		cpiFile   = jsonCoordsFile.replace ("Manifiesto", "Cartaporte")
		cpiCoords = json.load (open (cpiFile))
		docFile   = cpiFile.replace ("-Cartaporte","")

	docCoords = {"CARTAPORTE": cpiCoords, "MANIFIESTO": mciCoords}
	json.dump (docCoords, open (docFile, "w"), indent=4)
	

#--------------------------------------------------------------------
# Return PDF width and height
#--------------------------------------------------------------------
def getPdfSize (pdfFilename):
	import pdfplumber
	with pdfplumber.open(pdfFilename) as pdf:
		page = pdf.pages [0]
		width  = page.width
		height = page.height
		print(f"{width}, {height}")
		return width, height

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def convertPdfToImg (pdfFilepath):
	width, height = getPdfSize (pdfFilepath)
	outFile = pdfFilepath.split (".")[0] + f"-{width}x{height}" + ".png"
	cmm = ["convert", "-density", "150", pdfFilepath, "-resize", f"{width}x{height}", outFile]
	print (f"Convert command: ", cmm)
	subprocess.run (cmm)
	print (f"Output file:", outFile)
#--------------------------------------------------------------------
#--------------------------------------------------------------------
main ()

