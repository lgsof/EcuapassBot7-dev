#!/usr/bin/env python3
import sys, re
import pdfplumber

from ecuapassdocs.info.ecuapass_utils import Utils
from ecuapassdocs.info.ecuapass_data import EcuData
from ecuapassdocs.info.ecuapass_exceptions import EcudocPdfCoordinatesError 
from ecuapassdocs.info.resourceloader import ResourceLoader 

from scraping_doc import ScrapingDoc
 
#----------------------------------------------------------
# Scraping of doc fields from PDF document
#----------------------------------------------------------
class ScrapingDocPdf (ScrapingDoc):
	def __init__ (self, pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		super().__init__ (pdfFilepath, empresa, pais, distrito, credentials, runningDir)

	#----------------------------------------------------
	# Extract initial application fields (txt01, txt02,....)
	#----------------------------------------------------
	def extractAppFields (self):
		pdfCoordinates = self.getPdfCoordinates (self.pdfFilepath)

		appFields = {}
		with pdfplumber.open (self.pdfFilepath) as pdf:
			page = pdf.pages [0]
			for k, box in pdfCoordinates.items ():
				x0, y0, x1, y1 = box[0], box[1], box[0]+box[2], box[1]+box[3]  # Coordinates of the box
				cropped_page = page.within_bbox ((x0, y0, x1, y1))
				text = cropped_page.extract_text() if cropped_page else ""
				appFields [k] = text.strip() if text else ""

		self.checkEmpresaPermisos (appFields)

		Utils.saveFields (appFields, self.pdfFilepath, "APPFIELDS")
		return appFields

	#---------------------------------------------------------------- 
	# Return box coordinates from PDF document (CPI or MCI)
	# Coordinates file is defined in each subclass
	#---------------------------------------------------------------- 
	def getPdfCoordinates (self, pdfFilepath=None):
		coordinatesFile = EcuData.empresas [self.empresa]["coordsFile"]
		coords_CPI_MCI = ResourceLoader.loadJson ("docs", coordinatesFile)
		coords   = coords_CPI_MCI [self.docType]
		return coords

	#----------------------------------------------------------------
	# Check if is a valid 'empresa' by validating 'permiso'
	#----------------------------------------------------------------
	def checkEmpresaPermisos (self, appFields):
		permisoKeys  = {"CARTAPORTE": "txt0b", "MANIFIESTO": "txt02"}
		key          = permisoKeys [self.docType]
		permisoText  = appFields [key]
		EcuData.checkEmpresaPermisos (self.empresa, permisoText)

