#!/usr/bin/env python3

import os, sys, json, re, time
import PyPDF2

from info.ecuapass_utils    import Utils
from info.ecuapass_settings import Settings
from info.ecuapass_cloud    import EcuCloud 
from info.ecuapass_exceptions import EcudocException

from scraping         import ScrapingDoc

USAGE="\n\
Extract info from ECUAPASS documents in PDF (cartaporte|manifiesto|declaracion).\n\
USAGE: ecuapass_doc.py <PDF document>\n"

def main ():
	if (len (sys.argv) < 2):
		print (USAGE)
	else:
		pdfFilepath = sys.argv [1]
		runningDir = os.getcwd()
		EcuDoc.processDocument (pdfFilepath, runningDir, "SANCHEZPOLO", "COLOMBIA")

#-----------------------------------------------------------
# Run cloud analysis
#-----------------------------------------------------------
class EcuDoc:
	empresa = None
	docType = None

	#----------------------------------------------------------------
	#-- Analyze one document given its path
	# Extract fields info from PDF document (using CODEBIN bot)
	#----------------------------------------------------------------
	def processDocument (pdfFilepath, empresa, pais, distrito):
		try:
			# Get basic PDF info
			filename        = os.path.basename (pdfFilepath)
			EcuDoc.docType  = Utils.getDocumentTypeFromFilename (filename)
			EcuDoc.empresa  = empresa
			EcuDoc.pais     = pais
			print (f"+++ distrito '{distrito}'")

			# Start document processing for WEB or PDF document
			scrapingDoc    = ScrapingDoc.creatingScrapingDocObject (pdfFilepath, empresa, pais, distrito)
			appFields      = scrapingDoc.extractAppFields ()                   # Extract text from boxes in PDF or WEB document 
			docFieldsPath  = scrapingDoc.getDocFieldsFile (appFields)              # Convert appFields to docFields
			ecuFields      = scrapingDoc.extractEcuapassFields (docFieldsPath)

			# Send log
			EcuCloud.sendLog (Settings.empresa, Settings.version, pdfFilepath)

			response = f"EXITO: Documento procesado: '{pdfFilepath}'"

		except EcudocException as ex:
			Utils.printException ("Problemas procesando documento")
			response = str (ex)
		except:
			Utils.printException ("Problemas procesando documento")
			response = f"DOCERROR::Problemas procesando documento"

		return response


#	#------------------------------------------------------
#	# Get pdf info (empresa, pais, docType, docFields)
#	#------------------------------------------------------
#	def getPdfInfo (pdfFilepath):
#		ScrapingDocPdf = ScrapingDocPdf (EcuDoc.empresa, EcuDoc.docType, pdfFilepath)

	#----------------------------------------------------------------
	#-- Load previous document fields doc, if it exists
	#----------------------------------------------------------------
	def searchCacheAppFile (pdfFilepath):
		cacheFilename = f"{pdfFilepath.rsplit ('.', 1)[0]}-APPFIELDS.json"
		Utils.printx (f"Buscando documento cache '{cacheFilename}'...")
		if os.path.exists (cacheFilename): 
			Utils.printx (f"\t...Si existe documento cache : '{cacheFilename}'.")
			return cacheFilename
		else:
			Utils.printx (f"\t...No existe documento cache : '{cacheFilename}'.")
			return None

	#----------------------------------------------------------------
	#-- Get embedded fields info from PDF
	#----------------------------------------------------------------
	def getEmbeddedFieldsFromPDF (pdfPath):
		fieldsJsonPath = pdfPath.replace (".pdf", "-FIELDS.json")
		try:
			with open(pdfPath, 'rb') as pdf_file:
				pdf_reader = PyPDF2.PdfReader(pdf_file)

				# Assuming the hidden form field is added to the first page
				first_page = pdf_reader.pages[0]

				# Extract the hidden form field value 
				text     = first_page.extract_text()  
				jsonText = re.search ("Embedded_jsonData: ({.*})", text).group(1)
				Utils.printx ("Obteniendo campos desde el archivo PDF...")
				fieldsJsonDic  = json.loads (jsonText)
				json.dump (fieldsJsonDic, open (fieldsJsonPath, "w"), indent=4, sort_keys=True)
		except Exception as e:
			Utils.printx ("EXCEPCION: Leyendo campos embebidos en el documento PDF.")
			return None

		return (fieldsJsonPath)

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()
