
#!/usr/bin/env python3
"""
Uses a coordinate file for PDF coordinates.
"""

import os, sys, json
import fitz  # Form PyMuPDF. Added to pyinstaller hidden modules

from info.ecuapass_utils import Utils
from info.ecuapass_settings import Settings
from info.ecuapass_exceptions import EcudocPdfCoordinatesError
from info.ecuapass_exceptions import EcudocSettingsError
from info.resourceloader import ResourceLoader 

from .scraping_doc_pdf import ScrapingDocPdf

#--------------------------------------------------------------------
# Class for extracting 'dynamically' coordinates from a PDF 
#--------------------------------------------------------------------
class ScrapingDocPdf_Static (ScrapingDocPdf):
	def __init__ (self, pdfFilepath, empresa, pais, distrito):
		super().__init__ (pdfFilepath, empresa, pais, distrito)

	#---------------------------------------------------------------- 
	# Return box coordinates from PDF document (CPI or MCI)
	# Coordinates file is defined in each subclass
	#---------------------------------------------------------------- 
	def getPdfCoordinates (self, docType, pdfFilepath=None):
		coordinatesFile = Settings.getCoordinatesFile ()

		coords_CPI_MCI  = ResourceLoader.loadJson ("docs", coordinatesFile)

		coordsDoc       = coords_CPI_MCI [docType]
		coords          = {k : tuple (v) for k,v in coordsDoc.items()}
		return coords

