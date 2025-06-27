#!/usr/bin/env python3

import re, os, sys

from .ecuapass_info_cartaporte import CartaporteInfo
from .ecuapass_info_manifiesto import ManifiestoInfo
from .ecuapass_extractor import Extractor
from .ecuapass_utils import Utils

#----------------------------------------------------------
USAGE = "\
Extract information from application documents (PDF or Web)\n\
USAGE: ecuapass_info_cartaportes.py <Json fields document>\n"
#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv
	fieldsJsonFile = args [1]
	runningDir = os.getcwd ()
	mainFields = CartaporteInfo.extractEcuapassFields (fieldsJsonFile, runningDir)
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Base class for RODFRONTE's Cartaporte and Manifiesto
#----------------------------------------------------------
class BOTEROSOTO:
	def __init__ (self):
		self.urlPrefix       = "boterosoto"   # byza.corebd.net
		self.coordinatesFile = "coordinates_pdfs_docs_BOTEROSOTO.json"
		
#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_BOTEROSOTO (BOTEROSOTO, CartaporteInfo):
	def __init__ (self, empresa, pais, distrito):
		super().__init__()
		CartaporteInfo.__init__ (self, empresa, pais, distrito)

	#-------------------------------------------------------------------
	#-- Get subject info: nombre, dir, pais, ciudad, id, idNro ---------
	#-- BS format: <Nombre> <ID> <Direccion> <PaisCiudad> -----
	#-------------------------------------------------------------------
	def getSubjectInfo (self, key):
		text	= self.fields [key]

		# First find the document info which is our anchor point
		doc_match = re.search(r'(NIT|RUC)\s*[:#.]*\s*([\d.\-]+)', text, re.IGNORECASE)
		if not doc_match:
			return None
		
		doc_type = doc_match.group(1).upper()
		doc_number = doc_match.group(2)
		doc_start, doc_end = doc_match.span()
		
		# Extract company name (everything before the document info)
		company_name = text[:doc_start].strip()
		
		# The remaining text after document info
		remaining_text = text[doc_end:].strip()
		
		# Improved pattern to handle complex cases
		# Look for country first, then city before it, rest is address
		country_pattern = r'''
			(?:.*\s)?                # Optional preceding text
			([A-Za-zÁ-Úá-ú]+)        # City (word characters with accents)
			\s*                      # Optional whitespace
			(?:[, -]\s*)?            # Optional separator
			(COLOMBIA|ECUADOR|PERU)  # Country
			\s*$                     # End of string
		'''
		country_match = re.search(country_pattern, remaining_text, re.IGNORECASE | re.VERBOSE)
		
		if not country_match:
			return None
		
		city = country_match.group(1).strip()
		country = country_match.group(2).upper()
		
		# Find everything before the city/country match
		city_start = country_match.start(1)
		address = remaining_text[:city_start].strip()
		
		return {
			'nombre': company_name,
			'direccion': address,
			'ciudad': city,
			'pais': country,
			'tipoId': doc_type,
			'numeroId': doc_number
		}


#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_BOTEROSOTO (BOTEROSOTO, ManifiestoInfo):
	def __init__ (self, empresa, pais, distrito):
		super().__init__()
		ManifiestoInfo.__init__ (self, empresa, pais, distrito)

	#-- Extract numero cartaprote 
	def getNumeroCartaporte (self):
		text    = self.fields ["28_Mercancia_Cartaporte"]
		text    = text.replace ("\n","")
		numero  = Extractor.getNumeroDocumento (text)
		return numero

	#-- Extract tipo embalaje from field "cantidad" : "30_Mercancia_Bultos"
	def getMercanciaEmbalaje (self, docItemKeys):
		return Extractor.getTipoEmbalaje (self.fields [docItemKeys ["cantidad"]])

	#-- Only the first line
	def getMercanciaMarcas (self, docItemKeys):
		marcas = self.fields [docItemKeys ["marcas"]]
		marcas = marcas.split ("\n")[0]
		return marcas.strip() if marcas else "SIN MARCAS"
#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

