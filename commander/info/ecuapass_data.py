import os, re, importlib

from info.ecuapass_utils import Utils
from info.ecuapass_extractor import Extractor
from info.ecuapass_exceptions import IllegalEmpresaException

#-----------------------------------------------------------
# Main
#-----------------------------------------------------------
def main ():
	empresasList = EcuData.getNombreEmpresasActivasCodebin ()
	for e in empresasList:
		print ("+++", e)

#-----------------------------------------------------------
#-- Class containing data for filling Ecuapass document
#-----------------------------------------------------------
class EcuData:
	temporalDir = None

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	empresas = { 
		"BOTEROSOTO" : { 
			"activa"     : True,
			'id'         : "BOTEROSOTO",
			"nombre"     : "EDUARDO BOTERO SOTO S.A.",
			"direccion"  : "Carrera 42 No 75-63 Aut. Sur, Itagui",
			"idTipo"     : "NIT", 
			"idNumero"   : "890901321-5",
			"appType"    : "BOTEROSOTO",
			"permisos"   : {"originario":"PO-CO-0011-21", "servicios1":"", "servicios2":""},
			"coordsFile" : "coordinates_pdfs_docs_BOTEROSOTO.json",
			"token"      :  "890.901.321-5"
		},

		"TRANSCOMERINTER" : { 
			"activa"     : True,
			'id'         : "TRANSCOMERINTER",
			"nombre"     : "TRANSPORTE Y COMERCIO INTERNACIONAL - TRANSCOMERINTER CIA. LTDA.",
			"direccion"  : "MALDONADO Y LAS GRADAS",
			"idTipo"     : "RUC", 
			"idNumero"   : "1791121104001",
			"appType"    : "TRANSCOMERINTER",
			"permisos"   : {"originario":"PO-EC-0069-23", "servicios1":"", "servicios2":""},
			"token"      :  "1791121104001|20521424746";
		},

		"SANCHEZPOLO": {
			"activa"   : True,
			'id'       : "SANCHEZPOLO",
			"nombre"   : "TRANSPORTES SANCHEZ POLO DEL ECUADOR C.A.",
			"direccion": "AV. ORIENTAL Y CALLE DE LAS CLAUDIAS SECTOR EL OBELISCO DE TULCN A 200 MTS POR LA PANAMERICANA",
			"idTipo"   : "NIT", 
			"idNumero" : "890103161-1",
			"appType"  : "SANCHEZPOLO",
			"permisos" : {"originario":"PO-CO-0060-23", "servicios1":None},
			"token"    : "NIT. 890103161-1"
		},

		"ALDIA": {
			"activa"     : True,
			'id'         : "ALDIA",
			"nombre"     : "ALDIA SAS",
			"direccion"  : "AV GALO PLAZA LASSO N 68-100 Y AVELLANEDAS",
			"idTipo"     : "RUC", 
			"idNumero"   : "1791250060001",
			"appType"    : "ALDIA",
			"permisos"   : {"originario":"PO-EC-0083-23", "servicios1":"P.P.S-CO-0196-09"},
			"coordsFile" : "coordinates_pdfs_docs_ALDIA.json",
			"token"      : "TRANSERCARGA|SERCARGA"
		},

		"ALDIA::TRANSERCARGA": {
			"activa"   : True,
			'id'       : "ALDIA::TRANSERCARGA",
			"nombre"   : "TRANSERCARGA SAS",
			"direccion": "AV GALO PLAZA LASSO N 68-100 Y AVELLANEDAS",
			"idTipo"   : "RUC", 
			"idNumero" : "1791250060001",
			"appType"  : "ALDIA",
			"permisos" : {"originario":"PO-EC-0083-23", "servicios1":"P.P.S-CO-0196-09"},
			"coordsFile" : "coordinates_pdfs_docs_ALDIA.json",
			"token"      : "TRANSERCARGA"
		},
	
		"ALDIA::SERCARGA": {
			"activa"   : True,
			'id'       : "ALDIA::SERCARGA",
			"nombre"   : "SERCARGA S.A.S.",
			"direccion": "AV GALO PLAZA LASSO N 68-100 Y AVELLANEDAS",
			"idTipo"   : "RUC", 
			"idNumero" : "1792006880001",
			"appType"  : "ALDIA",
			"permisos" : {"originario":"PO-CO-0018-21", "servicios1":"PO-CO-0018-21"},
			"coordsFile" : "coordinates_pdfs_docs_ALDIA.json",
			"token"      : "SERCARGA"
		},

		"BYZA": {
			"activa"     : True,
			'id'         : "BYZA",
			"nombre"     : "MONTALVO TERAN LUIS ALFONSO",
			"direccion"  : "CARCHI / TULCAN / GONZALEZ SUAREZ / AV. CORAL S/N  Y LOS ALAMOS",
			"idTipo"     : "RUC", 
			"idNumero"   : "0400201414001",
			"appType"    : "CODEBIN",
			"permisos"   : {"originario":"PO-CO-0033-22", "servicios1": "PO-CO-0033-22"},
			"coordsFile" : "coordinates_pdfs_docs_CODEBIN.json",
			"token"      : "NIT: 900.168.467-2"
		},

		"LOGITRANS" : { 
			"activa"   : True,
			'id'       : "LOGITRANS",
			"nombre"   : "TRANSPORTES LOGITRANS-ACROS S.A.",
			"direccion": "CALDERON Y PARAGUAY",
			"idTipo"   : "RUC", 
			"idNumero" : "0491507748001",
			"appType"  : "CODEBIN",
			"permisos" : {"originario":"PO-EC-0005-20", "servicios1": "PO-EC-0005-20"},
			"coordsFile" : "coordinates_pdfs_docs_CODEBIN.json",
			"token"    : "RUC 0491507748001"
		},

		"AUTOMOTORESDELNORTE" : { 
			"activa"     : True,
			'id'         : "AUTOMOTORESDELNORTE",
			"nombre"     : "COOPERATIVA DE TRANSPORTE DE CARGA PESADA Y CAMIONES AUTOMOTORES DEL NORTE",
			"direccion"  : "PANAMERICANA SUR, SECTOR EL OBELISCO",
			"idTipo"     : "RUC", 
			"idNumero"   : "0490004122001",
			"appType"    : "CODEBIN",
			"permisos"   : {"originario":"PO-EC-0106-24", "servicios1":"", "servicios2":""},
			"coordsFile" : "coordinates_pdfs_docs_CODEBIN.json",
			"token"      : "automotorestulcan@gmail.com"
		},

		"CITRAPCAR" : { 
			"activa"     : True,
			'id'         : "CITRAPCAR",
			"nombre"     : "COMPAÑIA DE LA INDUSTRIA DEL TRANSPORTE PESADO DEL CARCHI CITRAPCAR S.A.",
			"direccion"  : "CALLE EL MORAL Y AV. VEINTIMILLA",
			"idTipo"     : "RUC", 
			"idNumero"   : "0491506474001",
			"appType"    : "CODEBIN",
			"permisos"   : {"originario":"PO-EC-0090-23", "servicios1":"", "servicios2":""},
			"coordsFile" : "coordinates_pdfs_docs_CODEBIN.json",
			"token"      : "citrapcarsa@gmail.com"
		},

		"AGENCOMEXCARGO" : { 
			"activa"     : True,
			'id'         : "AGENCOMEXCARGO",
			"nombre"     : "LOGISTICA Y TRANSPORTE AGENCOMEXCARGO S.A.",
			"direccion"  : "AVENIDA MANABI 62018 Y BRASIL",
			"idTipo"     : "RUC", 
			"idNumero"   : "0491516194001",
			"appType"    : "CODEBIN",
			"permisos"   : {"originario":"PO-EC-0037-21", "servicios1":"", "servicios2":""},
			"coordsFile" : "coordinates_pdfs_docs_CODEBIN.json",
			"token"      : "RUC: 0491516194001"
		},

		"ALCOMEXCARGO" : { 
			"activa"     : False,
			'id'         : "ALCOMEXCARGO",
			"nombre"     : "TRANSPORTE DE CARGA NACIONAL E INTERNACIONAL ALCOMEXCARGO S.A.",
			"direccion"  : "CALLE AV. SAN FRANCISCO INT.: REMIGIO CRESPO TORAL REF.",
			"idTipo"     : "RUC", 
			"idNumero"   : "0491523638001",
			"appType"    : "CODEBIN",
			"permisos"   : {"originario":"PO-EC-0091-23", "servicios1":"", "servicios2":""},
			"coordsFile" : "coordinates_pdfs_docs_CODEBIN.json"
		},

		"RODFRONTE" : { 
			"activa"     : False,
			'id'         : "RODFRONTE",
			"nombre"     : "TRANSPORTE PESADO RODFRONTE S.A.",
			"direccion"  : "ARGENTINA Y JUAN LEON MERA - TULCAN",
			"idTipo"     : "RUC", 
			"idNumero"   : "1792600863001",
			"appType"    : "CODEBIN",
			"permisos"   : {"originario":"PO-EC-0108-24", "servicios1":None},
			"coordsFile" : "coordinates_pdfs_docs_CODEBIN.json"
		},

		"NTA" : { 
			"activa"   : False,
			'id'         : "NTA",
			"nombre"     : "NUEVO TRANSPORTE DE AMERICA COMPAÑIA LIMITADA", 
			"direccion"  : "ARGENTINA Y JUAN LEON MERA - TULCAN",
			"idTipo"     : "RUC", 
			"idNumero"   : "1791834461001",
			"appType"  : "CODEBIN",
			"permisos" : {"originario":"C.I.-E.C.-0060-04",
				          "servicios1":"P.P.S.CO015905", "servicios2":"P.P.S.PE000210"},
			"coordsFile" : "coordinates_pdfs_docs_CODEBIN.json"
		}
	}

	configuracion = {
		"dias_cartaportes_recientes" : 4,
		"numero_documento_inicio" : 2000000,
		"num_zeros" : 5
	}

	procedureTypes = {"COLOMBIA":"IMPORTACION", "ECUADOR":"EXPORTACION", "PERU":"IMPORTACION"}

	def getEmpresaInfo (empresa):
		return EcuData.empresas [empresa]

	def getEmpresaId (empresa):
		return EcuData.empresas [empresa]["numeroId"]

	def getEmpresasCodebinActivas ():
		empresasDict = EcuData.empresas
		empresasNames = []
		for name, values in empresasDict.items ():
			if values ['activa'] and values ['appType']=='CODEBIN':
				empresasNames.append (name)
		return empresasNames

	#----------------------------------------------------------------
	# Check if is a valid 'empresa' by validating 'permiso'
	#----------------------------------------------------------------
	def checkEmpresaPermisos (empresa, permisoText):
		permisoEmpresa = None
		try:
			empresaInfo    = EcuData.getEmpresaInfo (empresa)
			permisoEmpresa = empresaInfo ["permisos"]["originario"]
			permiso        = Utils.removeSymbols (empresaInfo ["permisos"]["originario"])
			permisoText    = Utils.removeSymbols (permisoText)

			if not permiso and permiso not in permisoText:
				raise IllegalEmpresaException (f"SCRAPERROR::Permiso desconocido: '{permiso}' vs. '{permisoText}' ")

			if not empresaInfo ["activa"]:
				raise IllegalEmpresaException (f"SCRAPERROR::Empresa '{empresa}' no está activa!")
		except IllegalEmpresaException:
			Utils.printException ('SCRAPERROR::Empresa no reconocida:', empresa)
			raise
		except Exception as ex:
			Utils.printException ('Problemas validando la empresa:', empresa)
			raise IllegalEmpresaException (f"SCRAPERROR::Problemas validando empresa: '{empresa}'!") from ex

		return permisoEmpresa

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()
