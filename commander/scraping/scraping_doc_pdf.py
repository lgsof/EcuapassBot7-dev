#!/usr/bin/env python3
import sys, re, json
import pdfplumber
import fitz  # Form PyMuPDF. Added to pyinstaller hidden modules

from info.ecuapass_utils import Utils
from info.ecuapass_settings import Settings
from info.ecuapass_extractor import Extractor
from info.ecuapass_exceptions import EcudocException, EcudocPdfCoordinatesError, EcudocExtractionException
from info.resourceloader import ResourceLoader 

from .scraping_doc import ScrapingDoc
 
#----------------------------------------------------------
# Scraping of doc fields from PDF document
#----------------------------------------------------------
class ScrapingDocPdf (ScrapingDoc):
	def __init__ (self, pdfFilepath, empresa, pais, distrito):
		self.pdfPage = self.openPdfPage (pdfFilepath)
		super().__init__ (pdfFilepath, empresa, pais, distrito)

	#----------------------------------------------------
	# Open PDF and get first page
	#----------------------------------------------------
	def openPdfPage (self, pdfFilepath):
		document = fitz.open (pdfFilepath)
		pdfPage  = document [0]
		return pdfPage

	#-- Get docType from PDF region (top center PDF page)
	def extractDocType (self):
		try:
			width, height = self.pdfPage.rect.width, self.pdfPage.rect.height
			headerText    = self.getTextFromBox (self.pdfPage, [1, 1, width, height/8])
			docType       = Utils.getDocTypeFromText (headerText)

			if docType:
				return docType
			raise Exception ()
		except Exception as ex:
			Utils.printException ("PDFERROR::Problemas extrayendo el tipo de documento desde el PDF")
			raise EcudocExtractionException ("PDFERROR::Problemas extrayendo el tipo de documento desde el PDF") from ex
			
	#----------------------------------------------------
	# Extract initial application fields (txt01, txt02,....)
	#----------------------------------------------------
	def extractAppFields (self):
		try:
			pdfCoordinates = self.getPdfCoordinates (self.docType, self.pdfFilepath)

			appFields = {}
			with pdfplumber.open (self.pdfFilepath) as pdf:
				page = pdf.pages [0]
				for txtKey, boxItem in pdfCoordinates.items ():
					appFields [txtKey] = self.getTextFromMultiBox (page, boxItem)

			Utils.saveFields (appFields, self.pdfFilepath, "APPFIELDS")
		except Exception as e:
			raise EcudocPdfCoordinatesError ('PDFERROR::Problemas extrayendo campos desde el PDF.') from e
		return appFields

	#-- Get text or multitex from box or multibox, resp.
	def getTextFromMultiBox (self, page, boxItem):
		textFull = ""
		boxList  = boxItem if type(boxItem) is list else [boxItem]

		#-- For TRANSCOMERINTER: Only the first item if there are multiple CPIs in the MCI description
		for box in boxList [:1]:
			textFull      += "\n--------------\n" if textFull else ""
			x0, y0, x1, y1 = box[0], box[1], box[0] + box[2], box[1] + box[3]  # Coordinates x,y,W,H
			cropped_page   = page.within_bbox ((x0, y0, x1, y1))
			text           = cropped_page.extract_text() if cropped_page else ""
			textFull      += text 

		return textFull.strip() if textFull else ""


	#-- box :: [x0, y0, W, H]
	def getTextFromBox (self, page, box):
		textFull = ""
		# For fitz library
		x0, y0, x1, y1 = box[0], box[1], box[0] + box[2], box[1] + box[3]  # Coordinates x,y,W,H
		rect = fitz.Rect (x0, y0, x1, y1)    # Define region: rect = (x0, y0, x1, y1)
		text = page.get_text("text", clip=rect) # Extract text from the region
# 		# For pdfplumber librart
#		x0, y0, x1, y1 = box[0], box[1], box[0] + box[2], box[1] + box[3]  # Coordinates x,y,W,H
#		cropped_page   = page.within_bbox ((x0, y0, x1, y1))
#		text           = cropped_page.extract_text() if cropped_page else ""

		return text.strip() 

	#-----------------------------------------------------------
	#-- Get PDF initial info for GUI Validation (token, docType, docPais, docNumber) 
	#-----------------------------------------------------------
	def getInitialPdfInfo (self):
		print (f"+++ Obteniendo información inicial del PDF")
		pdfInfo = {}
		try:
			self.pdfFilepath = Utils.copyFileToDir (self.pdfFilepath, Settings.getDocumentsPath ())
			appFields        = self.extractAppFields ()		# Extract text from boxes in PDF or WEB document 
			docFields        = self.getDocFields (appFields)	# Get appFields to docFields
			docFieldsPath    = self.getDocFieldsFile (appFields)	# Get appFields to docFields
			iniDocFields     = self.extractInitialFields (docFieldsPath)

			pdfInfo ["docType"]    = iniDocFields ["00_DocType"] # Document type
			#pdfInfo ["docEmpresa"] = self.docInfo.checkEmpresaToken (docFields ["01_Transportista"])
			pdfInfo ["docEmpresa"] = iniDocFields ["00_DocEmpresa"]

			pdfInfo ["docPais"]	   = iniDocFields ["00_DocPais"]
			if not pdfInfo ["docPais"]:
				raise EcudocExtractionException (f"PDFERROR::No se pudo extraer país origen desde el PDF")
			pdfInfo ["docNumber"]  = iniDocFields ["00_Numero"]
			if not pdfInfo ["docNumber"]:
				raise EcudocExtractionException (f"PDFERROR::No se pudo extraer número del documento desde el PDF")

			# Check permisos
			Settings.checkEmpresaPermisos (docFields ["00_DocPermiso"])

			# Set pais to docInfo
			self.docInfo.pais = pdfInfo ["docPais"]

			return pdfInfo

		except EcudocException as ex:
			raise
		except Exception as ex:
			raise EcudocExtractionException ("PDFERROR::Problemas extrayendo información inicial desde el PDF") from ex



