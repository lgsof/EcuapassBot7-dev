#!/usr/bin/env python3
import os, sys, re, time

from info.ecuapass_utils import Utils
from info.ecuapass_settings import Settings
from info.ecuapass_exceptions import EcudocException
from info.ecuapass_exceptions import EcudocDocumentNotFoundException
from info.ecuapass_exceptions import EcudocConnectionNotOpenException

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from .scraping_doc_web import ScrapingDocWeb

#----------------------------------------------------------
# Scraping of doc fields from WEB document
#----------------------------------------------------------
class ScrapingDocWeb_CODEBIN (ScrapingDocWeb):
	def __init__ (self, pdfFilepath, empresa, pais, distrito):
		super().__init__ (pdfFilepath, empresa, pais, distrito)
		self.pais, self.codigoPais = Utils.getPaisCodigoFromDocNumber (self.docNumber)

	#----------------------------------------------------
	# Get app codebin fields : {codebinField:value}
	#----------------------------------------------------
	def getValuesFromForm (self, docForm):
		docNumber = self.docNumber

		paramFields = Utils.getParamFieldsForDocument (self.docType)
		codebinValues = {}
		for key in paramFields.keys():
			if not "codebinField" in paramFields [key].keys():
				continue

			codebinField = paramFields [key]["codebinField"]
			try:
				elem = docForm.find_element (By.NAME, codebinField)
				value = elem.get_attribute ("value")
				codebinValues [codebinField] = value
			except NoSuchElementException:
				print (f"...Elemento '{codebinField}'  no existe")
				pass

		# For MANIFIESTO: Get selected radio button 
		if self.docType == "CARTAPORTE":
			codebinValues ["nocpic"] = docNumber
		elif self.docType == "MANIFIESTO":
			codebinValues ["no"] = docNumber

			radio_group = docForm.find_elements (By.NAME, "r25")  # Assuming radio buttons have name="size"
			for radio_button in radio_group:
				codebinField = radio_button.get_attribute('id')
				if radio_button.is_selected():
					codebinValues [codebinField] = "X"
				else:
					codebinValues [codebinField] = ""

		return codebinValues

	#-------------------------------------------------------------------
	# Navigate to document search table from Codebin menu and submenu
	#-------------------------------------------------------------------
	def locateSearchSite (self):
		textMainmenu = self.webSettings ["menu"]
		textSubmenu  = self.webSettings ["submenu"]

		wait = WebDriverWait (self.webdriver, 5)
		# Select menu Carta Porte I
		cpi = wait.until (EC.presence_of_element_located ((By.PARTIAL_LINK_TEXT, textMainmenu)))
		cpi.click ()

		# Select submenu 'Lista'
		cpi_lista = wait.until (EC.presence_of_element_located ((By.XPATH, f"//a[contains(@href, '{textSubmenu}')]")))
		cpi_lista.click ()

		# Get and switch to frame 'Lista'
		cpi_lista_object = wait.until (EC.presence_of_element_located ((By.TAG_NAME, "object")))

		wait.until (EC.frame_to_be_available_and_switch_to_it (cpi_lista_object))
		time.sleep (1)

	#-------------------------------------------------------------------
	# Return document form with their values
	#-------------------------------------------------------------------
	def searchDocumentInSite (self, docNumber):
		# get the input search field
		wait         = WebDriverWait (self.webdriver, 5)
		searchField  = wait.until (EC.presence_of_element_located ((By.TAG_NAME, "input")))
		docsTable    = wait.until (EC.presence_of_element_located ((By.TAG_NAME, "table")))

		searchField.send_keys (docNumber)

		# Get table, get row, and extract id
		docId = self.getCodebinDocumentId (docsTable, docNumber)

		# Get CODEBIN link for document with docId
		documentUrl  = self.webSettings ["link"]
		self.webdriver.get (documentUrl % docId)

		# Get Codebin values from document form
		docForm       = self.webdriver.find_element (By.TAG_NAME, "form")
		return docForm

	#-------------------------------------------------------------------
	# Codebin enter session: open URL and click into "Continuar" button
	#-------------------------------------------------------------------
	def openWebsite (self):
		try:
			print (f"+++ CODEBIN: ...Abriendo sitio web de la empresa '{self.empresa}'")
			self.webdriver.get (self.urlWebsite)
			submit_button = self.webdriver.find_element (By.XPATH, "//input[@type='submit']")
			submit_button.click()

			# Open new window with login form, then switch to it
			time.sleep (2)
			winMenu = self.webdriver.window_handles [-1]
			self.webdriver.switch_to.window (winMenu)

		except Exception as ex:
			Utils.printException (ex)
			raise EcudocConnectionNotOpenException ()

	#-------------------------------------------------------------------
	# Returns the web driver after login into CODEBIN
	#-------------------------------------------------------------------
	def loginWebsite (self):
		print (f"+++ CODEBIN: ...Autenticándose con paIs : '{self.pais}'")
		# Login Form : fill user / password
		loginForm = self.webdriver.find_element (By.TAG_NAME, "form")
		userInput = loginForm.find_element (By.NAME, "user")
		userInput.send_keys (self.user)
		pswdInput = loginForm.find_element (By.NAME, "pass")
		pswdInput.send_keys (self.password)

		# Login Form:  Select pais (Importación or Exportación : Colombia or Ecuador)
		docSelectElement = self.webdriver.find_element (By.XPATH, "//select[@id='tipodoc']")
		docSelect = Select (docSelectElement)
		docSelect.select_by_value (self.pais)
		submit_button = loginForm.find_element (By.XPATH, "//input[@type='submit']")
		submit_button.click()

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def getCodebinDocumentId (self, docsTable, docNumber):
		docId   = None
		try:
			#table   = container.find_element (By.TAG_NAME, "table")
			docLink    = docsTable.find_element (By.PARTIAL_LINK_TEXT, docNumber)
			idText     = docLink.get_attribute ("onclick")
			textLink   = docLink.text
			docId      = re.findall (r"\d+", idText)[-1]

			Utils.printx (f"+++ CODEBIN: ...Documento buscado: '{docNumber}' : Documento encontrado: '{textLink}'")
			if docNumber != textLink.strip():
				raise EcudocDocumentNotFoundException (f"SCRAPERROR::Documento '{docNumber}' no encontrado")
		except selenium.common.exceptions.NoSuchElementException:
			raise EcudocDocumentNotFoundException (f"SCRAPERROR::Documento '{docNumber}' no encontrado")
		except EcudocException as ex:
			raise
		except:
			raise Exception ("SCRAPERROR::Problemas extrayendo ID de COREBD Web")
		return docId

	#-------------------------------------------------------------------
	# Return web settings/links for acceding to CODEBIN documents
	#-------------------------------------------------------------------
	def getWebSettings (self):
		urlPrefix   = self.docInfo.urlPrefix
		webSettings = {}
		webSettings ["urlWebsite"] = f"https://{urlPrefix}.corebd.net"

		if self.docType == "CARTAPORTE":
			webSettings ["link"]    = f"https://{urlPrefix}.corebd.net/1.cpi/nuevo.cpi.php?modo=3&idunico=%s"
			webSettings ["menu"]    = "Carta Porte I"
			webSettings ["submenu"] = "1.cpi/lista.cpi.php?todos=todos"
			webSettings ["urlPrefix"]  = "CPI"

		elif self.docType == "MANIFIESTO":
			webSettings ["link"]    = f"https://{urlPrefix}.corebd.net/2.mci/nuevo.mci.php?modo=3&idunico=%s"
			webSettings ["menu"]    = "Manifiesto de Carga"
			webSettings ["submenu"] = "2.mci/lista.mci.php?todos=todos"
			webSettings ["urlPrefix"]  = "MCI"
		else:
			print ("Tipo de documento no soportado:", self.docType)
		return webSettings

	#----------------------------------------------------------------
	# Return doc fields ({02_Remitente:"XXXX"} from codebin fields
	#----------------------------------------------------------------
	def getDocFields (self, codebinFields, X):
		docFields = super().getDocFields (codebinFields, "codebinField")
		docFields ["00_DocPermiso"] = Settings.configData ["permiso"]
		return docFields

	#------------------------------------------------------
	# Take into account pais and distrito
	#------------------------------------------------------
	def getUserPassword (self):
		settingsData = Settings.configData

		user, password, distrito = None, None, None
		if self.pais  == "COLOMBIA" and self.distrito == "TULCAN":
			user	  = settingsData ["userColombia"]
			password  = settingsData ["passwordColombia"]
		elif self.pais == "ECUADOR" and self.distrito == "TULCAN":
			user	  = settingsData ["userEcuador"]
			password  = settingsData ["passwordEcuador"]
		elif self.pais == "PERU" and self.distrito == "HUAQUILLAS":
			user	  = settingsData ["userPeru"]
			password  = settingsData ["passwordPeru"]
		elif self.pais == "ECUADOR" and self.distrito == "HUAQUILLAS":
			user	  = settingsData ["userPeru"]
			password  = settingsData ["passwordPeru"]
		else:
			raise EcudocWebException (f"WEBERROR::No exite usuario/clave para pais: {self.pais}, distrito: {self.distrito}")

		return user, password

#-----------------------------------------------------------
# Call to main
#-----------------------------------------------------------
if __name__ == "__main__":
	main()
