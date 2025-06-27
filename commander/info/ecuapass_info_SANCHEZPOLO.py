#!/usr/bin/env python3
"""
Child class for SANCHEZPOLO Doc Info Classes
"""

import os, sys, re

from .ecuapass_info_cartaporte import CartaporteInfo
from .ecuapass_info_manifiesto import ManifiestoInfo

from .ecuapass_extractor import Extractor
from .ecuapass_utils import Utils
from .resourceloader import ResourceLoader 

#----------------------------------------------------------
USAGE = "\
Extract dynamically PDF coordinates from SANCHEZPOLO's docs\n\
USAGE: ecuapass_info_cartaportes.py <Json fields document>\n"
#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv
	docFieldsPath = args [1]
	runningDir = os.getcwd ()
	CartaporteInfo = CartaporteAldia (docFieldsPath, runningDir)
	mainFields = CartaporteInfo.extractEcuapassFields ()
	Utils.saveFields (mainFields, docFieldsPath, "Results")

#----------------------------------------------------------
# Base class for SANCHEZPOLO's Cartaporte and Manifiesto
#----------------------------------------------------------
class SANCHEZPOLO :
	#-- Get MRN from special field ----------------------------------
	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["appMRN"])  # Special docField from appField

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_SANCHEZPOLO (SANCHEZPOLO, CartaporteInfo):
	def __init__ (self, empresa, pais, distrito):
		CartaporteInfo.__init__ (self, empresa, pais, distrito)
#		self.scrapingPdf = ScrapingPdf_SANCHEZPOLO_Cartaporte ()

	#-- Get doc number from docFields -------------------------------
	def getNumeroDocumento (self, docKey="00_Numero"):
		numero, text = None, None
		try:
			text      = self.fields [docKey]
			reNumeros = r"^(\S+).*?(\S+)$"
			match     = re.match (reNumeros, text)
			if match:
				numero  = match.group(2)
		except:
			Utils.printException (f"No se pudo obtener número documento desde text: '{text}'")
		return numero

#	#-------------------------------------------------------------------
#	# Return float value from Euro format. Overwritten from base class
#	#-------------------------------------------------------------------
#	def getFloatValue (self, gastosKey):
#		valueAmericanFormat = self.fields [gastosKey]
#		print (f"+++ getFloatValue '{valueAmericanFormat}'")
#		value = '' if not valueAmericanFormat else Utils.americanToFloatValue (valueAmericanFormat)
#		return value
#
#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_SANCHEZPOLO (SANCHEZPOLO, ManifiestoInfo):
	def __init__ (self, empresa, pais, distrito):
		ManifiestoInfo.__init__ (self, empresa, pais, distrito)
#		self.scrapingPdf = ScrapingPdf_SANCHEZPOLO_Manifiesto ()

	#-- Try to convert certificado text to valid certificado string
	#-- Not added 'CH' nor 'CRU' in docs for colombian vehicles 
	def preformatCertificadoString (self, text):
		print (f"+++ TSP::text '{text}'")
		certs       = text.split ()
		newCerts    = []

		if len (certs) == 1: 
			if not 'CH' in certs [0]:
				newCerts.append ('CH-' + certs [0])
			else:
				newCerts.append (certs [0])
		elif len (certs) == 2:
			if not 'CH' in certs [0]:
				newCerts.append ('CH-' + certs [0])
			else:
				newCerts.append (certs [0])
			if not 'CRU' in certs [1]:
				newCerts.append ('CRU-' + certs [1])
			else:
				newCerts.append (certs [1])

		newText = " ".join (newCerts)
		return newText


#	def formatCertificadoString (self, text, vehicleType):
#		if vehicleType == "VEHICULO" and text.startswith ("CO"):
#			text = 'CH-' + text
#		elif vehicleType == "REMOLQUE" and text.startswith ("CO-"):
#			text = 'CRU-' + text
#
#		certificadoString = super().formatCertificadoString (text, vehicleType)
#		return certificadoString

	def getMercanciaEmbalaje (self, docItemKeys):
		return Extractor.getTipoEmbalaje (self.fields ['30_Mercancia_Bultos'])
