#!/usr/bin/env python3
import os, sys, re, time, locale

from info.ecuapass_utils import Utils
from info.ecuapass_exceptions import EcudocDocumentNotFoundException, EcudocConnectionNotOpenException

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from .scraping_doc_web import ScrapingDocWeb

#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args   = sys.argv
	option = args [1]

	if "--download" in option:
		print ("+++ Downloading documents...")
		pdfFilepath       = args [2]
		webdriver         = ScrapingDocWeb_ALDIA.loadWebdriver ()
		botAldia          = ScrapingDocWeb_ALDIA (pdfFilepath)
		docFieldsFilename = botAldia.downloadDocument ()
		
#----------------------------------------------------------
# Bot for web scraping of Codebin documents
#----------------------------------------------------------
class ScrapingDocWeb_ALDIA (ScrapingDocWeb):
	def __init__ (self, pdfFilepath, empresa, pais, distrito):
		super().__init__ (pdfFilepath, empresa, pais, distrito)

	#-------------------------------------------------------------------
	# Return document form with their values
	#-------------------------------------------------------------------
	def searchDocumentInSite (self, docNumber):
		print (f"+++ ALDIA: ...Consultando document : '{docNumber}'")

		docForm       = self.webdriver.find_element (By.NAME, "forma")
		cpicField     = docForm.find_element (By.NAME, "caprntcrid_b")
		cpicField.send_keys (docNumber)
		cpicField.send_keys("Selenium Python" + Keys.RETURN)

		# Retry loop to ensure the elements are fresh after submit
		max_attempts = 10
		form_data = {}

		for attempt in range (max_attempts):
			print (f"+++ ...Esperando valores forma... '{attempt}'")
			try:
				# Locate the form element again
				docForm = self.webdriver.find_element (By.NAME, "forma")  # Replace with actual form identifier
				form_fields = docForm.find_elements (By.CSS_SELECTOR, "input, select, textarea")

				# Retrieve updated field values
				form_data = {field.get_attribute('name'): field.get_attribute('value') for field in form_fields}
				break  # Exit loop if successful

			except StaleElementReferenceException:
				# Wait briefly and retry
				time.sleep(1)

		return docForm

	#----------------------------------------------------
	# Get codebin fields : {codebinField:value}
	#----------------------------------------------------
	def getValuesFromForm (self, docForm):
		print (f"+++ ALDIA: ...Obteniendo valores")

		paramFields = Utils.getParamFieldsForDocument (self.docType)
		appFieldsDic = {}
		for key, params in paramFields.items ():
			appField = params ["aldiaField"]
			if not appField:
				continue

			# Multiple ALDIA fields can conform one app field
			appFieldKey, appFieldValues = None, None
			if not type (appField) is dict:
				appFieldKey, appFieldValues = appField, [appField]
			else:
				appFieldKey, appFieldValues = next (iter (appField.items())) 
		
			# Loop for fields create from multiple fields (e.g. F1 = F1+F2+F3)
			fieldValues = []
			for fieldName in appFieldValues:
				try:
					if not fieldName.startswith ("docField_"):
						elem   = docForm.find_element (By.NAME, fieldName)
						if elem.tag_name == "select":
							fieldValues.append  (Select (elem).first_selected_option.text)
						else:
							fieldValues.append  (elem.get_attribute ("value"))
				except:
					Utils.printException (f"+++ EXCEPCION procesando '{fieldName}'")

			value = ". ".join (fieldValues)
			appFieldsDic [appFieldKey] = value

		# Add missing app fields
		appFieldsDic = self.addOtros (appFieldsDic)
		appFieldsDic = self.addTotals (appFieldsDic, "REMITENTE")
		appFieldsDic = self.addTotals (appFieldsDic, "DESTINATARIO")
		appFieldsDic = self.addPais (appFieldsDic)

		return appFieldsDic

	#----------------------------------------------------
	# Add missing doc field: "Otros Gastos"
	#----------------------------------------------------
	def addOtros (self, appFieldsDic):
		appFieldsDic ["docField_otrasUnidades"] = None
		return appFieldsDic

	#----------------------------------------------------
	# Add pais to appFields got from form values
	#----------------------------------------------------
	def addPais (self, appFieldsDic):
		pais = "COLOMBIA" # Default
		infoPais = appFieldsDic ["caprntcrcampo2"].split ("\n")[-1].upper()   # last line Remitente 

		if "COLOMBIA" in infoPais:
			pais = "COLOMBIA"
		elif "ECUADOR" in infoPais:
			pais = "ECUADOR"
		elif "PERU" in infoPais:
			pais = "PERU"
		else:
			print ("+++ ERROR: País no definido desde los valores de la forma")

		appFieldsDic ["docField_pais"] = pais
		return appFieldsDic
			
	#----------------------------------------------------
	# Calculate totals from pagos and add to appFields
	#----------------------------------------------------
	def addTotals (self, appFieldsDic,  subjectType):
		subjectDic = {
			"REMITENTE": {
				"flete"         : "caprntcrfleteremitente",
				"seguro"        : "caprntcrseguroremitente",
				"otro"          : "caprntcrotroremitente",
				"appField"      : "docField_totalRemitente",
				"appFieldMoneda": "docField_totalRemitenteMoneda" },
			"DESTINATARIO": {
				"flete"          : "caprntcrfletedestinatario",
				"seguro"         : "caprntcrsegurodestinatario",
				"otro"           : "caprntcrotrodestinatario",
				"appField"       : "docField_totalDestinatario",
				"appFieldMoneda" : "docField_totalDestinatarioMoneda" },
		}


		locale.setlocale (locale.LC_ALL, 'en_US.UTF-8')
		valuesFields = subjectDic [subjectType]
		flete        = locale.atof (appFieldsDic [valuesFields ["flete"]])
		seguro       = locale.atof (appFieldsDic [valuesFields ["seguro"]])
		otro         = locale.atof (appFieldsDic [valuesFields ["otro"]])
		total        = flete + seguro + otro
		appFieldsDic [valuesFields ["appField"]]       = Utils.numberToAmericanFormat (total)
		appFieldsDic [valuesFields ["appFieldMoneda"]] = "DOLARES"

		return appFieldsDic

	#-------------------------------------------------------------------
	# Navigate to document search table from Codebin menu and submenu
	#-------------------------------------------------------------------
	def locateSearchSite (self):
		print (f"+++ ALDIA: ...Abriendo sitio web de consulta")
		urlBuscar = "https://siat.aldialogistica.net/aldia/modulos/cpic/index.php?Buscar=1&Ventana="
		self.webdriver.get (urlBuscar)

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def getUserPassword (self):
		user      = Settings.configData ["userColombia"]
		password  = Settings.configData ["passwordColombia"]
		return user, password

	#-------------------------------------------------------------------
	# Returns the web driver after login into CODEBIN
	#-------------------------------------------------------------------
	def loginWebsite (self):
		print (f"+++ ALDIA: ...Autenticándose con país:'{self.pais}'")
		print (f"+++ ALDIA: ...Autenticándose con user:'{self.user}'")
		print (f"+++ ALDIA: ...Autenticándose con paswd:'{self.password}'")
		# Login Form : fill user / password
		loginForm = self.webdriver.find_element (By.TAG_NAME, "form")

		# Locate and send login/password
		userInput = loginForm.find_element (By.NAME, "login")
		userInput.send_keys (self.user)
		pswdInput = loginForm.find_element (By.NAME, "password")
		pswdInput.send_keys (self.password)

		# Select associated company 
		wait = WebDriverWait (self.webdriver, 5)
		docSelectElement = wait.until (EC.presence_of_element_located ((By.XPATH, "//select[@id='datos']")))
		docSelect        = Select (docSelectElement)
		webdriver        = self.webdriver
		WebDriverWait (webdriver, 10).until(
			lambda webdriver: len (docSelect.options) > 0  # Wait until there is at least one option
		)
		docSelect.select_by_visible_text (self.webSettings ["associatedCompany"])

		# Submit 
		submit_button = loginForm.find_element (By.NAME, "BDoLogin")
		submit_button.click()

	#-------------------------------------------------------------------
	# Codebin enter session: open URL and click into "Continuar" button
	#-------------------------------------------------------------------
	def openWebsite (self):
		try:
			print (f"+++ ALDIA: ...Abriendo sitio web de la empresa '{self.empresa}'...")
			self.webdriver.get (self.webSettings ["urlWebsite"])
#			submit_button = self.webdriver.find_element(By.XPATH, "//input[@type='submit']")
#			submit_button.click()
#
#			# Open new window with login form, then switch to it
#			time.sleep (2)
#			winMenu = self.webdriver.window_handles [-1]
#			self.webdriver.switch_to.window (winMenu)

		except Exception as ex:
			Utils.printException (ex)
			raise EcudocConnectionNotOpenException ()

	#-------------------------------------------------------------------
	# Return Web links for the current company and document type
	#-------------------------------------------------------------------
	def getWebSettings (self):
		webSettings = {}
		webSettings ["urlWebsite"] = "https://siat.aldialogistica.net/aldia/modulos/cpic/index.php"
		webSettings ["associatedCompany"] = "01 SERCARGA SAS"
		webSettings ["urlCartaporte"] = "https://siat.aldialogistica.net/aldia/modulos/cpic/index.php"   

		return webSettings

	#----------------------------------------------------------------
	# Return doc fields ({02_Remitente:"XXXX"} from aldia fields
	#----------------------------------------------------------------
	def getDocFields (self, aldiaFields):
		return super().getDocFields (aldiaFields, "aldiaField")

#-----------------------------------------------------------
# Call to main
#-----------------------------------------------------------
if __name__ == "__main__":
	main()
