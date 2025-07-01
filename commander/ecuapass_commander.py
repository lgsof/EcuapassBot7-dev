#!/usr/bin/env python3

VERSION="0.972"
"""
LOG: 
Mar/27: 0.972: Modified CPI Gastos/Unidades Values (ALDIA, TSP)
Nov/29 : 0.964 : Working for SANCHEZPOLO. Working ScrapingWeb.
"""

import os, sys, time, json, threading

from info.ecuapass_utils import Utils
from info.ecuapass_info import EcuInfo
from info.ecuapass_exceptions import *
from version import APP_VERSION

from info.ecuapass_cloud   import EcuCloud 
from info.ecuapass_settings import Settings    # Config class 

from ecuapass_doc import EcuDoc
from ecuapass_bot import EcuBot
from scraping     import ScrapingDocWeb
from scraping     import ScrapingDoc

#----------------------------------------------------------------
# Definitions
#----------------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')

#----------------------------------------------------------------
# Listen for remote calls from Java GUI
# Called with the running dir as unique argument
#----------------------------------------------------------------
def main ():
	# Override the default exception handler
	#sys.excepthook = global_exception_handler    # Exceptions to cloud

	# Notify the caller (Java) that the process is ready
	print (f"Python executable is ready to receive commands. ({getAppVersion()})", flush=True)

	while True:
		try:
			# Read input from Java client
			params = input().strip().split("|")
			print (f"+++ params: '{params:}'")
			if 'exit' in params:
				sys.exit (0)

			service = params [0]
			param1, param2, param3, param4 = params [1], params [2], params [3], params [4]

			response = None
			# Set initial app values: empresa, version, runningDir
			if service == "init_application":
				response = EcuCmm.initApplication (empresa=param1, version=getAppVersion (), runningDir=param2)

			elif service == "get_initial_pdf_info":
				response = EcuCmm.getInitialPdfInfo (pdfFilepath=param1, empresa=param2)

			elif service == "get_installkey_cloud":
				installKey = EcuCloud.getInstallKey (empresa=param1)
				response = f"CLOUDINSTKEY::{installKey}"

			elif service == "doc_processing":
				response = EcuCmm.docProcessing (pdfFilepath=param1, empresa=param2, pais=param3, distrito=param4)

			elif service == "bot_init_transmission":
				response = EcuCmm.botInitTransmission (empresa=param1, ecuFieldsFilepath=param2, runningDir=param3)

			elif (service == "bot_init_typing"):
				response = EcuCmm.botInitTyping (empresa=param1, ecuFieldsFilepath=param2, 
									             runningDir=param3, coordinatesString=param4)

			elif (service == "codebin_transmit"):
				response = EcuCmm.codebin_transmit (workingDir=param1, codebinFieldsFile=param2)

			elif (service == "ecuapassdocs_transmit"):
				response = EcuCmm.ecuapassdocs_transmit (workingDir=param1, ecuapassdocsFieldsFile=param2)

			elif (service == "open_ecuapassdocs_URL"):
				EcuCmm.openEcuapassdocsURL (url=param1)

			elif (service == "stop_application"):
				response = EcuCmm.stop_application (runningDir=param1)

			# When settings (data, config) are modified from GUI 
			elif (service == "settings_updated"):
				response = EcuCmm.settings_updated ()

			elif (service == "exit"):
				sys.exit (0)

			elif (service == "is_running"):
				response = "true"

			else:
				response = f"BOTERROR:: Servicio '{service}' no existe."

		except EcudocException as ex:
			response = str (ex)
		except Exception as ex:
			Utils.printException ('Error desconocido')
			response = f"DOCERROR::No se pudo procesar documento:\\\\{str(ex)}"
			sys.exit (0)

		response = f"RESPONSE::{response}"
		print (response, flush=True)

#-----------------------------------------------------------
# Get App version from global README.md file
#-----------------------------------------------------------
def getAppVersion ():
	version = 'r1.00'
	try:
		versionFilepath = os.path.join (os.getcwd(), "README.md")
		lines = open (versionFilepath).readlines ()
		for i,l in enumerate (lines):
			if 'LOG' in l:
				firstLogLine = lines [i+1]
				version  = firstLogLine.split (':')[1].split (':')[0].strip()
				return version
	except Exception as ex :
		pass

	return version

#-----------------------------------------------------------
# Exceptions to cloud
#-----------------------------------------------------------
def global_exception_handler (exc_type, exc_value, exc_traceback):
	print (f"+++ in global_exception_handler...")
	error_time = datetime.now().isoformat()
	error_msg = f"[{error_time}] Unhandled exception:\n"
	error_msg += "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
	
	# Log to Google Sheets (or Drive)
	# log_error_to_google_sheets (error_msg)	# Your existing logging function
	EcuCloud.sendLog (Settings.empresa, Settings.version, error_msg, logSheet='errors')	# Your existing logging function
	
	# Optional: Also print to console (helpful for debugging)
	print (error_msg, file=sys.stderr)
	
	# Call the original handler (optional)
	#sys.__excepthook__(exc_type, exc_value, exc_traceback)

#-----------------------------------------------------------
# EcuCmm: listen GUI messages, run processes, and respond to GUI
#-----------------------------------------------------------
class EcuCmm:
	errorsList = []
	cmmThread  = None

	# Set initial app values: empresa, version, runningDir
	def initApplication (empresa, version, runningDir):
		Settings.init (empresa, version, runningDir)
		Settings.reload ()
		EcuCmm.cmmThread = threading.Thread (target=EcuCloud.checkDowloadPatchFromGit, args=[])
		EcuCmm.cmmThread.start()
		EcuCmm.cmmThread = threading.Thread (target=EcuCloud.checkAuthorizedEmpresa, args=[empresa, EcuCmm.errorsList])
		EcuCmm.cmmThread.start()
		print (f"+++ Verificando si empresa '{empresa}' está autorizada...")
		response = "Applicación iniciada!"
		return response
	            
	def getInitialPdfInfo (pdfFilepath, empresa):
		EcuCmm.cmmThread.join ()
		for e in EcuCmm.errorsList:
			raise e
		scrapingPdf       = ScrapingDoc.creatingScrapingDocObject (pdfFilepath, empresa, None, None)
		pdfInfo           = scrapingPdf.getInitialPdfInfo ()
		pdfInfoResponse   = {"initialPdfInfo" : pdfInfo}
		pdfInfoJsonString = json.dumps (pdfInfoResponse)
		return pdfInfoJsonString
	
	def docProcessing (pdfFilepath, empresa, pais, distrito):
		#EcuCmm.cmmThread.join ()
		#for e in EcuCmm.errorsList:
		#	raise e
		response = EcuDoc.processDocument (pdfFilepath, empresa, pais, distrito)
		return response
		
	#----------------------------------------------------------------
	#-- Execute bot according to the document type
	#-- Doctype is in the first prefix of the ecuFieldsFilepath
	#----------------------------------------------------------------
	def botInitTyping (empresa, ecuFieldsFilepath, runningDir, coordinatesString):
		try:
			bot = EcuBot.createBot_OBJECT (empresa, ecuFieldsFilepath, runningDir, coordinatesString)
			bot.activateEcuapassWindow ()

			bot.mouseController.confine_mouse ()
			bot.locateOnMenuIzquierdo ()
			bot.fillEcuapass ()
			bot.mouseController.release_mouse ()
			#EcuCmm.fillEcuapassBlockingHard (bot)
			return "Documento digitado"

		except EcudocTypingError as ex:
			raise 

		except EcudocBotCartaporteNotFound as ex:
			return "BOTERROR::Cartaporte no encontrada: seleccionela manualmente!"
		except EcudocBotStopException as ex:
			return "BOTERROR::Digitación interrumpida"
		except EcuerrorImageNotFound as ex:
			return "BOTERROR::Ventana ECUAPASS no está lista: Imágen 'Menu Izquierdo' no visible"
		
		except Exception as ex:
			Utils.printException ('Error digitando documento en ECUAPASS')
			return f"BOTERROR::Error digitando documento en ECUAPASS"
		finally:
			from mouse_controller import MouseController
			MouseController.RELEASE_MOUSE ()

	#----------------------------------------------------------------
	# It needs windows admin permissions
	#----------------------------------------------------------------
	def fillEcuapassBlockingHard (bot):
		import ctypes
		try:
			# Block all user input (mouse + keyboard)
			ctypes.windll.user32.BlockInput(True)
			bot.fillEcuapass ()
		finally:
			# Always unblock input!
			ctypes.windll.user32.BlockInput(False)

	#----------------------------------------------------------------
	# Activate ECUAPASS window
	#----------------------------------------------------------------
	def botInitTransmission (empresa, ecuFieldsFilepath, runningDir):
		try:
			Utils.printx ("+++ Iniciando bot processing...")
			EcuInfo.prepareUpdateFieldsFile (ecuFieldsFilepath)

			bot = EcuBot (empresa, ecuFieldsFilepath, runningDir, 'CARTAPORTE') 
			bot.activateEcuapassWindow ()
			return "Ventana de ECUAPASS activada!"
		except EcudocException as ex:
			raise
		except Exception as ex:
			message = f"BOTERROR::Problemas activando ventana de ECUAPASS:\\\\{str(ex)}"
			Utils.printException (message)
			return message

	#-- Stop application
	def stop_application (runningDir):
		print (f"+++ Finalizando aplicación")
		ScrapingDocWeb.quitWebdriver ()
		return "Aplicación Finalizada"
		#sys.exit (0)

	#----------------------------------------------------------------
	#-- Transmit document fields to CODEBIN web app using Selenium
	#----------------------------------------------------------------
	def codebin_transmit (workingDir, codebinFieldsFile):
		from bot_codebin import startCodebinBot
		filepath = os.path.join (workingDir, codebinFieldsFile)
		docType = Utils.getDocumentTypeFromFilename (codebinFieldsFile)
		startCodebinBot (docType, filepath)

	#----------------------------------------------------------------
	#-- Transmit document fields to ECUAPASSDOCS web app using Selenium
	#----------------------------------------------------------------
	def ecuapassdocs_transmit (workingDir, ecuapassdocsFieldsFile):
		from bot_ecuapassdocs import startEcuapassdocsBot
		filepath = os.path.join (workingDir, ecuapassdocsFieldsFile)
		docType = Utils.getDocumentTypeFromFilename (ecuapassdocsFieldsFile)
		startEcuapassdocsBot (filepath)

	#----------------------------------------------------------------
	# Settings updated in GUI (data and config)
	#----------------------------------------------------------------
	def settings_updated ():
		Settings.reload ()
		return "Settings actualizadas"



#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()
