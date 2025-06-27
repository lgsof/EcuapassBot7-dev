#!/usr/bin/env python3

import os, sys, re

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
class CITRAPCAR:
	def __init__ (self):
		self.urlPrefix       = "citrapcar"   # byza.corebd.net

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_CITRAPCAR (CITRAPCAR, CartaporteInfo):
	def __init__ (self, empresa, pais, distrito):
		super().__init__()
		CartaporteInfo.__init__ (self, empresa, pais, distrito)

	#-- get MRN according to empresa and docField
	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["22_Observaciones"])

	#-- In CITRAPCAR: Deposito in first line of field 05_Notificado
	def getDepositoMercancia (self):
		try:
			text         = self.fields ["05_Notificado"]
			lineDeposito = text.split ("\n")[0]
			reBodega     = r'(\b\w+)'
			bodega       = Extractor.getValueRE (reBodega, lineDeposito)
			depositosDic = Extractor.getDataDic ("depositos_tulcan.txt", self.resourcesPath)
			for id, textBodega in depositosDic.items ():
				if bodega in textBodega:
					print (f"+++ Deposito '{id}' : '{textBodega}'")
					return id
			raise
		except:
			Utils.printException (f"+++ No se puedo obtener deposito desde texto '{text}'")
			return "||LOW"
#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_CITRAPCAR (CITRAPCAR, ManifiestoInfo):
	def __init__ (self, empresa, pais, distrito):
		super().__init__()
		ManifiestoInfo.__init__ (self, empresa, pais, distrito)

	#-- get MRN according to empresa and docField
	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["29_Mercancia_Descripcion"])

	#-- Extract only the fist paragraph text
	def getMercanciaDescripcion (self, docItemKeys):
		docFieldKey  = docItemKeys ["descripcion"]
		descripcion  = self.fields [docFieldKey]

		if self.docType == "CARTAPORTE":   # Before "---" or CEC##### or "\n"
			pattern = r'((\n\n).*)$'
			descripcion = re.sub (pattern, "", descripcion, flags=re.DOTALL)

		elif self.docType == "MANIFIESTO": # Before "---" or CPI: ###-###
			pattern = r'((REMITE:|\n\n).*)$'
			descripcion = re.sub (pattern, "", descripcion, flags=re.DOTALL)

		return descripcion.strip()

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

