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
class AUTOMOTORESDELNORTE:
	def __init__ (self):
		self.urlPrefix       = "automotoresdelnorte"   # byza.corebd.net

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_AUTOMOTORESDELNORTE (AUTOMOTORESDELNORTE, CartaporteInfo):
	def __init__ (self, empresa, pais, distrito):
		super().__init__()
		CartaporteInfo.__init__ (self, empresa, pais, distrito)

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_AUTOMOTORESDELNORTE (AUTOMOTORESDELNORTE, ManifiestoInfo):
	def __init__ (self, empresa, pais, distrito):
		super().__init__()
		ManifiestoInfo.__init__ (self, empresa, pais, distrito)

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

