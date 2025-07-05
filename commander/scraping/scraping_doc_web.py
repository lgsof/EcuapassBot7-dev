#!/usr/bin/env python3

"""
Fill CODEBIN web form from JSON fields document.
"""
import sys, json, re, time, os
import PyPDF2

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, NoSuchWindowException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Browser webdrivers
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from info.ecuapass_utils import Utils
from .scraping_doc import ScrapingDoc
from info.ecuapass_settings import Settings

from info.ecuapass_exceptions import EcudocDocumentNotFoundException
from info.ecuapass_exceptions import EcudocConnectionNotOpenException
from info.ecuapass_exceptions import EcudocWebException

#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv

	# Load "empresa": reads and checks if "settings.txt" file exists')
	runningDir     = os.getcwd ()

	pdfFilepath       = args [1]
	runningDir        = os.getcwd()

	scrapingWeb       = ScrapingDocWeb.createClass (pdfFilepath, "BYZA", "COLOMBIA", "TULCAN")
	print (f"+++ scrapingWeb type: '{type(scrapingWeb)}'")

	appFields         = scrapingWeb.extractAppFields ()
	Utils.saveFields (appFields, pdfFilepath, "APPFIELDS")
		
#--------------------------------------------------------------------
# Base class for Scraping Web classes
#--------------------------------------------------------------------
class ScrapingDocWeb (ScrapingDoc):
	def __init__ (self, pdfFilepath, empresa, pais, distrito):
		super().__init__ (pdfFilepath, empresa, pais, distrito)
		self.urlWeb          = Settings.datos ["urlWeb"]
		self.user, self.password = self.getUserPassword ()
		self.webSettings         = None       # Defined in child classes
		ScrapingDocWeb.loadWebdriver ()
	
	#----------------------------------------------------------------
	#----------------------------------------------------------------
	def extractDocType (self):
		return Utils.getDocTypeFromText (self.pdfFilepath)

	#----------------------------------------------------------------
	# Extract initial application fields (txt01, txt02,....)
	# Download doc fields from website (Codebin, Aldia, ....)
	#----------------------------------------------------------------
	def extractAppFields (self):
		try:
			self.webSettings  = self.getWebSettings ()    # Child implementation
			if self.downloadingSameTypeDocs ():
				print ("+++ Website: ...Regresando...")
				self.webdriver.back ()    # Search results
			else:
				print ("+++ Website: ...Iniciando...")
				# Call to bot to get values from CODEBIN web
				self.initWebdriver ()
				self.openWebsite ()                           # Child implementation
				self.loginWebsite ()                          # Child implementation
				# Set flags
				ScrapingDocWeb.IS_OPEN   = True
				ScrapingDocWeb.LAST_PAIS = self.pais
				ScrapingDocWeb.DOC_FOUND = False

			self.locateSearchSite ()                          # Child implementation
			docForm   = self.searchDocumentInSite (self.docNumber)
			appFields = self.getValuesFromForm (docForm)
			# Update flags
			ScrapingDocWeb.IS_OPEN   = True
			ScrapingDocWeb.LAST_PAIS = self.pais
			ScrapingDocWeb.DOC_FOUND = True

			Utils.saveFields (appFields, self.pdfFilepath, "APPFIELDS")
			return appFields

		except EcudocDocumentNotFoundException:
			ScrapingDocWeb.DOC_FOUND = False
			raise 
		except (EcudocConnectionNotOpenException, NoSuchWindowException, InvalidSessionIdException):
			self.quitWebdriver ()
			raise EcudocConnectionNotOpenException ("WEBERROR::No se pudo conectar a la Web. Intentelo nuevamente")
		except:
			self.quitWebdriver ()
			raise Exception ("WEBERROR::No se pudo conectar a la Web. Intentelo nuevamente")


		return None
	#-------------------------------------------------------------------
	# Initial browser opening
	# Open codebin session for new docs or go back to begina a new search
	#-------------------------------------------------------------------
	def initWebdriver (self):
		try:
			if ScrapingDocWeb.webdriver == None:
				Utils.printx ("+++ Website: Cargando nuevamente el webdriver...")
				ScrapingDocWeb.startWebdriver ()
			self.webdriver = ScrapingDocWeb.webdriver
		except Exception as ex:
			Utils.printException (ex)
			raise EcudocConnectionNotOpenException () from ex

	#-- Keep downloading same type documents
	def downloadingSameTypeDocs (self):
		if ScrapingDocWeb.webdriver and ScrapingDocWeb.DOC_FOUND \
		   and ScrapingDocWeb.IS_OPEN and ScrapingDocWeb.LAST_PAIS == self.pais:
			return True

		return False

	#------------------------------------------------------
	# Load webdriver 
	# Static as it is called in background in analyze_docs
	#------------------------------------------------------
	@staticmethod
	def loadWebdriver ():
		Utils.printx ("Loading webdriver...")
		# Load the webdriver
		while not hasattr (ScrapingDocWeb, "webdriver"):
			ScrapingDocWeb.startWebdriver ()
			ScrapingDocWeb.IS_OPEN = False
			ScrapingDocWeb.LAST_PAIS = ""
			ScrapingDocWeb.DOC_FOUND = False
			#ScrapingDocWeb.webdriver = webdriver.Firefox ()
		return ScrapingDocWeb.webdriver

	#-- Start webdriver, with options, from browser driver
	def startWebdriver ():
		Utils.printx ("\n...Starting webdriver...")
		#------------- Firefox webdriver ----------------
		options = Options()
		#options.add_argument("--headless")
		ScrapingDocWeb.webdriver = webdriver.Firefox (options=options)

		#------------- Chrome webdriver -----------------
		#options = webdriver.ChromeOptions()
		# Configure Chrome options
		# Set the User-Agent string to mimic Firefox 34
		#options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:34.0) Gecko/20100101 Firefox/34.0")
		#options.add_argument("--headless")  # Use this if you still need headless mode
		#ScrapingDocWeb.webdriver = webdriver.Chrome (service=Service(ChromeDriverManager().install()), options=options)

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	@staticmethod
	def quitWebdriver ():
		#-- Webdriver is killed by the main function as it is an independent thread
		if hasattr (ScrapingDocWeb, "webdriver"):
			print ("+++ Quitando webdriver")
			ScrapingDocWeb.webdriver.quit ()

		ScrapingDocWeb.IS_OPEN   = False
		ScrapingDocWeb.LAST_PAIS = ""
		ScrapingDocWeb.DOC_FOUND = False
		ScrapingDocWeb.webdriver = None

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	@classmethod
	def buscarEmpresaCodebini (cls, codebiniId):
		cls.loadWebdriver ()
		driver = cls.webdriver
		url = f"https://{codebiniId.lower()}.corebd.net"

		driver.set_page_load_timeout(15)
		try:
			driver.get (url)
			title = driver.title
		except Exception as ex:
			Utils.printException ("No se pudo extraer nombre empresa desde página Codebini:", codebiniId)
			title = "", ""
		finally:
			driver.quit()
			del cls.webdriver
			
		return title, url


#-----------------------------------------------------------
# Call to main
#-----------------------------------------------------------
if __name__ == "__main__":
	main()
