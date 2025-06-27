import os

from info.ecuapass_info import EcuInfo
from info.ecuapass_utils import Utils
from info.resourceloader import ResourceLoader

from info.ecuapass_exceptions import EcudocException 
from info.ecuapass_exceptions import EcudocPdfCoordinatesError 
from info.ecuapass_exceptions import EcudocWebException
from info.ecuapass_settings import Settings

#--------------------------------------------------------------------
# Base class for PDF and WEB scraping
#--------------------------------------------------------------------
class ScrapingDoc:
	def __init__ (self, pdfFilepath, empresa, pais, distrito):
		self.pdfFilepath = pdfFilepath
		self.docType     = self.extractDocType ()
		self.empresa	 = empresa
		self.pais		 = pais
		self.distrito	 = distrito

		self.docInfo	 = EcuInfo.createDocInfoInstance (empresa, self.docType, pais, distrito)

		if pais != None:
			self.docType	 = Utils.getDocumentTypeFromFilename (pdfFilepath)
			self.docNumber	 = Utils.getDocumentNumberFromFilename (pdfFilepath) 

	#----------------------------------------------------------------
	# Create ScrapingDocWeb or ScrapinDocPdf classes for "empresa"
	#----------------------------------------------------------------
	@staticmethod
	def creatingScrapingDocObject (pdfFilepath, empresa, pais, distrito):
		try:
			filename = os.path.basename (pdfFilepath)
			scrapingDocCLASS = None
			if "DUMMY" in pdfFilepath:
				Utils.printx (f">>>>>>>>>>>>>> Procesando documento WEB: '{filename}' <<<<<<<<<<<<<<<<<")
				scrapingDocCLASS = ScrapingDoc.createDocWebClass (pdfFilepath, empresa, pais, distrito)
			else:
				Utils.printx (f">>>>>>>>>>>>>> Procesando documento PDF: '{filename}' <<<<<<<<<<<<<<<<<")
				scrapingDocCLASS = ScrapingDoc.createDocPdfClass (pdfFilepath, empresa, pais, distrito)

			return scrapingDocCLASS
		except EcudocException:
			raise
		except Exception as ex:
			raise EcudocPdfCoordinatesError (f"SCRAPERROR::Problemas alistando acceso a documentos por WEB o PDF") from ex

	#----------------------------------------------------------------
	# Return child ScrapingDocPdf class for specific "empresa"
	#----------------------------------------------------------------
	@staticmethod
	def createDocPdfClass (pdfFilepath, empresa, pais, distrito):
		scrapingObj = None
		if 'BOTEROSOTO' in empresa:
			from .scraping_doc_pdf_BOTEROSOTO import ScrapingDocPdf_BOTEROSOTO
			scrapingObj = ScrapingDocPdf_BOTEROSOTO (pdfFilepath, empresa, pais, distrito)
		elif 'ALDIA' in empresa:
			from .scraping_doc_pdf_ALDIA import ScrapingDocPdf_ALDIA
			scrapingObj = ScrapingDocPdf_ALDIA (pdfFilepath, empresa, pais, distrito)
		elif 'TRANSCOMERINTER' in empresa:
			from .scraping_doc_pdf_dynamic_TRANSCOMERINTER import ScrapingDocPdfDynamic_TRANSCOMERINTER
			scrapingObj = ScrapingDocPdfDynamic_TRANSCOMERINTER (pdfFilepath, empresa, pais, distrito)
		elif 'SANCHEZPOLO' in empresa:
			from .scraping_doc_pdf_dynamic_SANCHEZPOLO import ScrapingDocPdfDynamic_SANCHEZPOLO
			scrapingObj = ScrapingDocPdfDynamic_SANCHEZPOLO (pdfFilepath, empresa, pais, distrito)
		else: 
			from .scraping_doc_pdf_static import ScrapingDocPdf_Static
			scrapingObj = ScrapingDocPdf_Static (pdfFilepath, empresa, pais, distrito)

		return scrapingObj

	#----------------------------------------------------------------
	# Return child ScrapingDocWeb class for specific "empresa"
	#----------------------------------------------------------------
	@staticmethod
	def createDocWebClass (pdfFilepath, empresa, pais, distrito):
		scrapingObj = None
		if Settings.hasCodebinWebAccess (): # BYZA, AGENCOMEXCARGO, LOGITRANS, CITRAPCAR
			from .scraping_doc_web_CODEBIN import ScrapingDocWeb_CODEBIN
			scrapingObj = ScrapingDocWeb_CODEBIN (pdfFilepath, empresa, pais, distrito)
			return scrapingObj
		elif empresa in ["ALDIA::TRANSERCARGA", "ALDIA::SERCARGA"]:
			from .scraping_doc_web_ALDIA import ScrapingDocWeb_ALDIA
			scrapingObj = ScrapingDocWeb_ALDIA (pdfFilepath, empresa, pais, distrito)
			return scrapingObj
		else:
			raise EcudocWebException (f"WEBERROR::Empresa '{empresa}' no tiene acceso Web")

	#----------------------------------------------------------------------
	# Get docFields from appFields according to appFields source in PARAMS
	# AppFields sources: "ecudocsField", "codebinField", or "aldiaField"
	#----------------------------------------------------------------------
	def getDocFields (self, appFields, APPTYPE="appField"):
		docFields	   = Utils.getDocFieldsFromAppFields (appFields, self.docType, APPTYPE)
		return docFields

	def getDocFieldsFile (self, appFields, APPTYPE="appField"):
		docFields	   = self.getDocFields (appFields, APPTYPE)
		docFieldsPath  = Utils.saveFields (docFields, self.pdfFilepath, "DOCFIELDS")
		return docFieldsPath

#	# Abstract: implemente in subclasses
#	def extractDocType (self):
#		raise Exception ("ERROR::Funcion NO implementada")
	#----------------------------------------------------
	# Extract Ecuapass fields from app fields
	#----------------------------------------------------
	def extractEcuapassFields (self, docFieldsPath):
		return self.extractEcuapassFieldsByType (docFieldsPath, "ECUFIELDS")

	def extractInitialFields (self, docFieldsPath):
		return self.extractEcuapassFieldsByType (docFieldsPath, "INIFIELDS")

	def extractEcuapassFieldsByType (self, docFieldsPath, KEYTYPE="ECUFIELDS"):
		logFile, stdoutOrg = Utils.redirectOutput (f"log-extraction-{self.docType}-{KEYTYPE}.log")
		try:
			self.docInfo.setDistrito (self.distrito)

			ecuFields = self.docInfo.extractEcuapassFields (docFieldsPath)
			if KEYTYPE == "ECUFIELDS":
				ecuFields = {k:v for k, v in ecuFields.items() if not k.startswith ("00")}
			elif KEYTYPE == "INIFIELDS":
				ecuFields = {k:v for k, v in ecuFields.items() if k.startswith ("00")}
			else:
				raise Exception ("ERROR::Problemas extrayendo campos Ecuapass")

			#ecuFieldsPath  = Utils.saveFields (ecuFields, self.pdfFilepath, KEYTYPE)

			docFieldsPath  = os.path.join (Settings.getDocumentsPath (), os.path.basename (self.pdfFilepath))
			ecuFieldsPath  = Utils.saveFields (ecuFields, docFieldsPath, KEYTYPE)
			return ecuFields
		except EcudocException as ex:
			raise
		except:
			message = f"DOCERROR::Problemas extrayendo EcuapassFields"
			Utils.printException (message)
			raise Exception (message)
		finally:
			Utils.redirectOutput ("log-extraction-cartaporte.log", logFile, stdoutOrg)

#	#------------------------------------------------------
#	# Take into account pais and distrito
#	#------------------------------------------------------
#	def getUserPassword (self):
#		settings = Settings.readBinSettings ()
#
#		user, password, distrito = None, None, None
#		if self.pais  == "COLOMBIA" and self.distrito == "TULCAN":
#			user	  = settings ["userColombia"]
#			password  = settings ["passwordColombia"]
#		elif self.pais == "ECUADOR" and self.distrito == "TULCAN":
#			user	  = settings ["userEcuador"]
#			password  = settings ["passwordEcuador"]
#		elif self.pais == "PERU" and self.distrito == "HUAQUILLAS":
#			user	  = settings ["userPeru"]
#			password  = settings ["passwordPeru"]
#		elif self.pais == "ECUADOR" and self.distrito == "HUAQUILLAS":
#			user	  = settings ["userPeru"]
#			password  = settings ["passwordPeru"]
#		else:
#			raise EcudocWebException (f"WEBERROR::No exite usuario/clave para pais: {self.pais}, distrito: {self.distrito}")
#
#		return user, password
#
