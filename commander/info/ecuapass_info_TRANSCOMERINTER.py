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
class TRANSCOMERINTER:
	def __init__ (self):
		self.urlPrefix       = "transcomerinter"   # byza.corebd.net
		self.coordinatesFile = "coordinates_pdfs_docs_TRANSCOMERINTER.json"

	def getMercanciaEmbalaje (self, docItemKeys):
		return Extractor.getTipoEmbalaje (self.fields [docItemKeys ["marcas"]])

	def getMercanciaMarcas (self, docItemKeys):
		return "S/M"

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_TRANSCOMERINTER (TRANSCOMERINTER, CartaporteInfo):
	def __init__ (self, empresa, pais, distrito):
		super().__init__()
		CartaporteInfo.__init__ (self, empresa, pais, distrito)

	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["22_Observaciones"])  # Special docField from appField

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_TRANSCOMERINTER (TRANSCOMERINTER, ManifiestoInfo):
	def __init__ (self, empresa, pais, distrito):
		super().__init__()
		ManifiestoInfo.__init__ (self, empresa, pais, distrito)

#	def getMercanciaDescripcion (self, docItemKeys):
#		return self.fields ['appDescripcion']

	#-----------------------------------------------------------
	# Get info from unidades de medida:"peso neto, volumente, otras
	#-----------------------------------------------------------
	def getTotalUnidadesInfoManifiesto (self):
		itemKeys = {'pesoNeto':'32a_Peso_BrutoTotal', 'pesoBruto':'32b_Peso_NetoTotal', 
				       'volumen':None, 'otraMedida':'33_Otra_MedidaTotal'}
		return super ().getTotalUnidadesInfo (itemKeys)

	#-----------------------------------------------------------
	#-- Overwritten: 32a:PesoNeto, 32b:PesoBruto Get mercancia info: cantidad, embalaje, marcas
	#-----------------------------------------------------------
	def getMercanciaInfoManifiesto (self):
		docItemKeys = {'cartaporte':'28_Mercancia_Cartaporte', "descripcion": "29_Mercancia_Descripcion",
				       "cantidad": "30_Mercancia_Bultos", "marcas": "31_Mercancia_Embalaje", "embalaje": '31_Mercancia_Embalaje',
				       'pesoNeto':'32a_Peso_Bruto', 'pesoBruto':'32b_Peso_Neto', 'otraMedida':'33_Otra_Medida'}

		mercanciaInfo = super().getMercanciaInfo (docItemKeys)
		mercanciaInfo ["cartaporte"] = self.getNumeroCartaporte ()
		return mercanciaInfo

	def getFechaNacimiento (self, text):
		fecha_nacimiento = Extractor.getDate ('1990/04/01', self.resourcesPath) + "||LOW"
		print (f"+++ MCI::getFechaNacimiento::fecha_nacimiento '{fecha_nacimiento}'")
		return fecha_nacimiento

	#-- Conductor's licencia equals to documento
	def extractConductorInfo (self, type="CONDUCTOR"):
		conductor = super().extractConductorInfo (type)
		conductor ['licencia'] = conductor ['documento']
		return conductor

	#-- '0' if empty, for PERU
	def getPrecintosInfo (self, docFieldKey):
		precintosItemsString = Extractor.getItemsFromTextList (self.fields [docFieldKey])
		print (f"\n+++ precintosItemsString '{precintosItemsString}'")
		if precintosItemsString == '' and 'PERU' in self.ecudoc ["47_Pais_Carga"]:
			precintosItemsString = '0'
		return precintosItemsString

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

