import os

from ecuapassdocs.info.ecuapass_info import EcuInfo
from ecuapassdocs.info.ecuapass_data import EcuData
from ecuapassdocs.info.ecuapass_utils import Utils
from ecuapassdocs.info.resourceloader import ResourceLoader
from ecuapassdocs.info.ecuapass_exceptions import EcudocPdfCoordinatesError 

#--------------------------------------------------------------------
# Base class for PDF and WEB scraping
#--------------------------------------------------------------------
class ScrapingDoc:
	def __init__ (self, pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		self.pdfFilepath = pdfFilepath
		self.empresa     = empresa
		self.pais        = pais
		self.distrito    = distrito
		self.credentials = credentials
		self.runningDir  = runningDir

		self.docType     = Utils.getDocumentTypeFromFilename (pdfFilepath)
		self.docNumber   = Utils.getDocumentNumberFromFilename (pdfFilepath) # Special for NTA
		self.docInfo     = EcuInfo.createDocInfoInstance (self.docType, empresa, pais, runningDir)

	#----------------------------------------------------------------
	# Create ScrapingDocWeb or ScrapinDocPdf classes for "empresa"
	#----------------------------------------------------------------
	@staticmethod
	def createClass (pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		try:
			filename = os.path.basename (pdfFilepath)
			scrapingDocCLASS = None
			if "DUMMY" in pdfFilepath:
				Utils.printx (f">>>>>>>>>>>>>> Procesando documento WEB: '{filename}' <<<<<<<<<<<<<<<<<")
				scrapingDocCLASS = ScrapingDoc.createDocWebClass (pdfFilepath, empresa, pais, distrito, credentials, runningDir)
			else:
				Utils.printx (f">>>>>>>>>>>>>> Procesando documento PDF: '{filename}' <<<<<<<<<<<<<<<<<")
				scrapingDocCLASS = ScrapingDoc.createDocPdfClass (pdfFilepath, empresa, pais, distrito, credentials, runningDir)

			return scrapingDocCLASS
		except:
			Utils.printException ()
			raise EcudocPdfCoordinatesError (f"SCRAPERROR::Problemas obteniendo coordenadas documento de la empresa '{empresa}'")

	#----------------------------------------------------------------
	# Return child ScrapingDocWeb class for specific "empresa"
	#----------------------------------------------------------------
	@staticmethod
	def createDocPdfClass (pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		scrapingObj = None
		if 'ALDIA' in empresa:
			from scraping_doc_pdf_ALDIA import ScrapingDocPdf_ALDIA
			scrapingObj = ScrapingDocPdf_ALDIA (pdfFilepath, empresa, pais, distrito, credentials, runningDir)
		elif 'SANCHEZPOLO' in empresa:
			from scraping_doc_pdf_SANCHEZPOLO import ScrapingDocPdf_SANCHEZPOLO
			scrapingObj = ScrapingDocPdf_SANCHEZPOLO (pdfFilepath, empresa, pais, distrito, credentials, runningDir)
		else: 
			from scraping_doc_pdf import ScrapingDocPdf
			scrapingObj = ScrapingDocPdf (pdfFilepath, empresa, pais, distrito, credentials, runningDir)

		return scrapingObj

	#----------------------------------------------------------------
	# Return child ScrapingDocWeb class for specific "empresa"
	#----------------------------------------------------------------
	@staticmethod
	def createDocWebClass (pdfFilepath, empresa, pais, distrito, credentials, runningDir):
		scrapingObj = None
		#if empresa in ["BYZA", "AGENCOMEXCARGO", "LOGITRANS"]:
		if empresa in EcuData.getEmpresasCodebinActivas (): # BYZA, AGENCOMEXCARGO, LOGITRANS, CITRAPCAR
			from scraping_doc_web_CODEBIN import ScrapingDocWeb_CODEBIN
			scrapingObj = ScrapingDocWeb_CODEBIN (pdfFilepath, empresa, pais, distrito, credentials, runningDir)
			return scrapingObj
		elif empresa in ["ALDIA::TRANSERCARGA", "ALDIA::SERCARGA"]:
			from scraping_doc_web_ALDIA import ScrapingDocWeb_ALDIA
			scrapingObj = ScrapingDocWeb_ALDIA (pdfFilepath, empresa, pais, distrito, credentials, runningDir)
			return scrapingObj
		else:
			raise EcudocWebException (f"ACCESSERROR::Empresa '{empresa}' no tiene acceso Web")

	#----------------------------------------------------
	# Extract Ecuapass fields from app fields
	#----------------------------------------------------
	def extractEcuapassFields (self, docFieldsPath):
		try:
			self.docInfo.setDistrito (self.distrito)

			# Extract fields
			ecuFields      = self.docInfo.extractFields (docFieldsPath)
			ecuFieldsPath  = Utils.saveFields (ecuFields, self.pdfFilepath, "ECUFIELDS")
			return ecuFields
		except:
			Utils.printException ()
			raise Exception (f"Problemas extrayendo EcuapassFields'")

	#------------------------------------------------------
	# Take into account pais and distrito
	#------------------------------------------------------
	def getUserPassword (self):
		user, password, distrito = None, None, None
		if self.pais  == "COLOMBIA" and self.distrito == "TULCAN":
			user      = self.credentials ["userColombia"]
			password  = self.credentials ["passwordColombia"]
		elif self.pais == "ECUADOR" and self.distrito == "TULCAN":
			user      = self.credentials ["userEcuador"]
			password  = self.credentials ["passwordEcuador"]
		elif self.pais == "PERU" and self.distrito == "HUAQUILLAS":
			user      = self.credentials ["userPeru"]
			password  = self.credentials ["passwordPeru"]
		elif self.pais == "ECUADOR" and self.distrito == "HUAQUILLAS":
			user      = self.credentials ["userPeru"]
			password  = self.credentials ["passwordPeru"]
		else:
			raise Exception (f"No exite usuario/clave para pais: {self.pais}, distrito: {self.distrito}")

		return user, password

	#----------------------------------------------------
	# Get docFields from appFields (01_Remitente, 02_Destinatario,...)
	#----------------------------------------------------
	def getDocFields (self, appFields):
		docFields      = Utils.getDocFieldsFromAppFields (appFields, self.docType, "appField")
		docFieldsPath  = Utils.saveFields (docFields, self.pdfFilepath, "DOCFIELDS")
		return docFieldsPath


