#!/usr/bin/env python3
import sys, re
import pdfplumber

from info.ecuapass_utils import Utils
from info.ecuapass_settings import Settings
from info.ecuapass_exceptions import EcudocPdfCoordinatesError
from info.resourceloader import ResourceLoader 

from .scraping_doc_pdf import ScrapingDocPdf
 
#----------------------------------------------------------
# Scraping of doc fields from PDF document
#----------------------------------------------------------
class ScrapingDocPdf_ALDIA (ScrapingDocPdf):
	def __init__ (self, pdfFilepath, empresa, pais, distrito):
		super().__init__ (pdfFilepath, empresa, pais, distrito)

	#----------------------------------------------------------------
	# Coordinates for ALDIA doc has it has two sets of Manifiesto docs
	#----------------------------------------------------------------
	def getPdfCoordinates (self, docType, pdfFilepath=None):
		coordinatesFile = Settings.getCoordinatesFile ()
		coords_CPI_MCI  = ResourceLoader.loadJson ("docs", coordinatesFile)
		coords = {}

		if docType == 'MANIFIESTO':
			with pdfplumber.open (self.pdfFilepath) as pdf:
				page = pdf.pages [0]
				print(f"+++ Page width: {page.width}, Height: {page.height}")
				if page.height == 877:   # Default Manifiesto::Only one CPI
					coords = coords_CPI_MCI ['MANIFIESTO']['NORMAL']
				elif page.height == 792: # Special Manifiesto::Two CPIs
					coords = coords_CPI_MCI ['MANIFIESTO']['DOS_CPIs']
				else:
					raise EcudocPdfCoordinatesError (f"PDFERROR::Coordenadas errones del Manifiesto PDF: {page.width}x{page.height}")
		else:
			coords = coords_CPI_MCI [docType]

		coords   = {k : tuple (v) for k,v in coords.items()}
		return coords 
