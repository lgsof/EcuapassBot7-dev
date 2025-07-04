#!/usr/bin/env python3

"""
Send and get data from google cloud
"""

import os, sys, threading
from datetime import datetime
import base64, json
import requests    # For updates using github release assets

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from google.auth.exceptions import TransportError
import httplib2, socket
from googleapiclient.errors import HttpError

from info.ecuapass_exceptions import EcudocCloudException
from info.ecuapass_exceptions import EcuerrorNetworkConnection
from info.ecuapass_exceptions import EcudocException
from info.ecuapass_exceptions import IllegalEmpresaException

from info.ecuapass_utils import Utils
from info.ecuapass_settings import Settings

#----------------------------------------------------------------
# Main for test
#----------------------------------------------------------------
def main ():

	# Send log info
	#EcuCloud.sendLog ('BYZA', "Hola-Como-Estas.json", logType="errors")

	# Send log PDF
	EcuCloud.sendLog ('BYZA', 'r1.01', 'CPIC-TRANSCOMERINTER-TEST-0060000000913.pdf')
	print (f"+++ Log sent")

#	# Validate user
#	username = 'BYZA'
#	if EcuCloud.validate_user (username):
#		print(f'User {username} is valid.')
#	else:
#		print(f'User {username} is invalid.')

#----------------------------------------------------------------
# Class for sending message logs and files to Azure blob
#----------------------------------------------------------------

class EcuCloud:
	logFile         = "EcuapassBot-Logs-01"
	pdfsFolderId    = '1KMj34j4XEdWPmJ7l3Gkeg18y9MUTGOcw'
	#errorsGoogleSheetFile    = "EcuapassBot-Errors"
	googleKeyString = "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiY29yZS1mYWxjb24tNDQ1OTE2LW0xIiwKICAicHJpdmF0ZV9rZXlfaWQiOiAiZWExNWNhMjEwNjM0NDM2NDhhZTliY2FkODIzODAyMWQzYmQyNTJmZCIsCiAgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLVxuTUlJRXZBSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS1l3Z2dTaUFnRUFBb0lCQVFDeVV4dEZEZVBUVjFuWFxucHFYQzhGR3RGdExKV2hIc1JJeFNnZ3R1ODVna0pHajJ1RVJvQTNLNlNwNG53RHNSb3Vpa3pFQm1EaEgxQk8zblxubzVIUjJrelBhd1BrSHE1SzZIcGxyazdxSTZzWlpuMzNLWlpqalBYQ25FdDNUODRlVzhObytFcHhlNUVkYlRHalxudzVBeW1OdngyK2tGVWNsT0F1N3FjOEM5bWM5MDd5SjZVU1g1ZHE1SXE4WjdFRURRRVdIc0g4SHN5M0JhUjZPSlxuYWZ5TDFMVmErUGhXZ2dIdlFzU2trS3RRanRVbXRQaW9zOU0xOGZCVTdVRmF4bFROVUJ1QW5GRy9qM0xaN3loZ1xucVVTa1VPYUhUSGp0blZRUVhCNEdWY1VxaWhJQ2FaNjh1M2RWcHZZSTRrNnN0MDBJaW5Ma0hUUDZSaGF6MXNJNlxua0pSd2xnOHRBZ01CQUFFQ2dnRUFMeGN3TTllYnFyTStCK3M3aWRPQmxoWlpXbys4L09vTExqeW1QVW41aXMzTVxucEI1Ny9nV3ZGYy9mblBxdi9wUEpJTC9KWDhubVp4QkNyUEZ1Yi83WVdzdlZUcmZsYWVXamNOZUxnbHdoOGthMVxuREFDQTlOQUVGRHpHMXY2Tm5VbTVQQzZaSmdldUJoblFTb0U1d29ySVJrRys4c2NxeEQyVkR2ZTdWYlpZNlBWTlxuRGRUQ0JsNk1qTlNNOHU4S2NuNnZJZ3VJa1dHdHh3VmptZWxqZWY2TWwzbkdsRkg2dmxQM0ZZaDFTOHZHWDFuelxuUS84dDF1UEhncUFzUTNhSEErVEJJaTVZbnR1MUdOclJ2Y3h2MFA4TU5IaHJERk1hbmxybjZpbEovNFJJTTh3ZlxubnYxTkF4WllNR0NKVWlLcmNjTjZSOE9mOFFUbk5UU3A3ZnVXd1hJMkJ3S0JnUUQ3UngzZUJYMERnWjlxak03RFxuZmNiOXhaOGlWZWRSZnhmNkkxYkM5NkhYbnZEUGFHMzFBb3hxQTAyZEl4WTF2MGtUZUhQYXJUSGp3dEIwQ3M3clxuWklpaTB2aDBmYjcvQUpmQlZKM0Q4b2dpb3JiNG9SSGxzZFpIckd3bnFkOXhOMlJROXpuWXNoUnRWdFprMk9zZFxuTGJYSmJjWGRXQVdZektRa3JZOEVaNHBma3dLQmdRQzFyUVFybGxVa2tCdmJiSjRrVFVnUkpCYS9QdTcxOThFMVxuQW9KcFg3N1QrS2pOTmNDeUpmQ2k1WnU4bWtmeVdWZU1CYlZpdzBuTll6Zi92SnBhMDA3Z3p2V3MweHJvelZMMFxud1FCM1VUZEFoaE5EZWtIcVF1WHNTWFh3UE9ScENsT0MwSDJhaFdCYTM2UFRYT25VUlRPNjl4WDcxbXN0dExxWFxuRC9JZHVvZU9Qd0tCZ0JUTDNmenlGMWFpODc2dHlLOEZTZUxXNkVTL04xWFhYdlNrMkJscXhVcERMVXI5S1p5TlxuaVhGOHRIKzgxNm03R3lFeFp1VkNVRTY1WU9jNXZjWmRtN0ZlSkpIL2xqOGtuV3F5eGh2aGhzTFhGSzJmSnd3TFxubStCeXRNRFRubHFRYXcwSWFSRTJLOXFneFQyemRrSUQ5bmVsVGlyempnTUhiTTVjVHVuZVorVmhBb0dBVWMxZVxudEZXVGJzd29qdXRnWlk0YXBnVXU3TnZrY3dJa2o3N2FnNkhsNWNId0Y3NWRUcG5BdVVoVGtGK1RoNjdzdVpLVVxuY3F6bUhVSFFwQ2tEQTJSai90dVJTVWtnczdSSDV3YkVNL1Z3d0cvZVdxTEE3VDlFRWRtZDdoY3M3Wk1GdVVBeFxuWGhNeUtKak1SazV1eHZLRjhXaHlFSndpVkVrdFB2bWlGZnE0TUxjQ2dZQk5scjZJRUhhOUszN0NidVJVSDJKRFxuMDI4bTZua01DTjhrUmNZL3M5Y1p3WlZWK29VSnRFZytQVzdoeFBFRGJDeVJRcWdOZzBGZWFCd0x1ZWV1NVdTNlxuTkdPS2ZYcHhBM3pjM3JvZTgyN3RsWHhBZmswQlVjWEE3eVlnTlUzTGUvemF4R1haZ2hTSkloK2Iva3hoQ1lHeVxuZ1BRekFaQlVHdnBjdlJFeG5LQ0M1QT09XG4tLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tXG4iLAogICJjbGllbnRfZW1haWwiOiAiZWN1YXBhc3Nib3QtbG9nc0Bjb3JlLWZhbGNvbi00NDU5MTYtbTEuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJjbGllbnRfaWQiOiAiMTE1MDc1NTIwMjk1NTg5Njk3NDEzIiwKICAiYXV0aF91cmkiOiAiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tL28vb2F1dGgyL2F1dGgiLAogICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLAogICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwKICAiY2xpZW50X3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vcm9ib3QvdjEvbWV0YWRhdGEveDUwOS9lY3VhcGFzc2JvdC1sb2dzJTQwY29yZS1mYWxjb24tNDQ1OTE2LW0xLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAidW5pdmVyc2VfZG9tYWluIjogImdvb2dsZWFwaXMuY29tIgp9Cg=="

	# For app updates (patchs in github releases)
	GITUSER     = "lgsof"
	GITREPO     = "EcuapassBot7-win"
	PATCHESLOG  = "patches/patches.log"

	# Flags for verification of authorized empresa
	authorizedEmpresaError = None
	authorizedEmpresaDone  = threading.Event ()
	
	#----------------------------------------------------------------
	# Trigger the logging asynchronously
	# logInfo: Text info or PDF filepath
	# logType: sheet name or 'PDF' for a shared PDFs folder
	#----------------------------------------------------------------
	def sendLog (empresa, version, logInfo, logType="logs"):
		thread = threading.Thread (target=EcuCloud.log_to_google_sheets, args=[empresa, version, logInfo, logType])
		thread.start()

	#-- Write docFilename to google logFile sheet
	def log_to_google_sheets (empresa, version, logInfo, logType):
		try:
			credentials = EcuCloud.getGoogleCredentials ()
			if logType == 'logs':      
				pdfFilepath = logInfo
				if empresa == 'TRANSCOMERINTER':
					EcuCloud.sendPdf (pdfFilepath, EcuCloud.pdfsFolderId, credentials)

				filename    = os.path.basename (pdfFilepath).split (".")[0]
				sheet       = EcuCloud.getGoogleSheet (logType, credentials)
				timestamp   = EcuCloud.getCurrentDateTimeString ()
				sheet.append_row ([empresa, filename, timestamp, version])
		except Exception as ex:
			print (f"EXCEPCION: enviando log a la nube: '{ex}'")



	#-- Upload PDF file to google drive folder 
	def sendPdf (pdfPath, folderId, credentials):
			file_metadata = {
				'name': os.path.basename (pdfPath),
				'mimeType': 'application/pdf',
				'parents' : [folderId]
			}

			# Build the service
			media   = MediaFileUpload(pdfPath, mimetype='application/pdf')
			service = build('drive', 'v3', credentials=credentials)	


			# Print google IM account
			about = service.about().get(fields="user").execute()
			print(f"Logged in as: {about['user']['emailAddress']}")
			
			file    = service.files().create(
						body=file_metadata,
						media_body=media,
						fields='id'
			).execute()

			print(f"PDF uploaded with ID: {file.get('id')}")
			return file.get('id')

	#-- Print exception to cloud with added 'message' and 'text'
	def printException (message="", text=None):
		if message:
			Utils.printx ("EXCEPCION: ", message) 
		if text:
			Utils.printx ("TEXT:", text) 

		stackTrace = ''.join(traceback.format_exc())
		orgMessage = f"{message}:\n{stackTrace}"
		Utils.printx (orgMessage)

		EcuCloud.sendLog (Settings.empresa, Settings.version, orgMessage, logType="errors")
	
	#-- Get google credentials
	def getGoogleCredentials ():
		scope       = [
			'https://spreadsheets.google.com/feeds',
			'https://www.googleapis.com/auth/drive'
		]
		gString     = EcuCloud.getDecodedString ()
		credentials = ServiceAccountCredentials.from_json_keyfile_dict (gString, scope)
		return credentials

	#-- Get sheet from google docs
	def getGoogleSheet (sheetName, credentials, logType="LOG"):
		#scope       = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		#gString     = EcuCloud.getDecodedString ()
		#credentials = ServiceAccountCredentials.from_json_keyfile_dict (gString, scope)
		client      = gspread.authorize (credentials)
		sheet       = client.open (EcuCloud.logFile).worksheet (sheetName)
		return sheet
	
	# Check if empresa is authorized or no
	def checkAuthorizedEmpresa (empresa, errorsList):
		try:
			credentials = EcuCloud.getGoogleCredentials ()
			sheet       = EcuCloud.getGoogleSheet ('clients', credentials)
			records     = sheet.get_all_records()
			for record in records:
				if record.get ("EMPRESA") == empresa:
					if record.get("AUTORIZACION", "").strip().upper() == "SI":
						print (f"+++++++++++++++ Empresa '{empresa}' está autorizada ++++++++++++++++", flush=True)
						return True
					else:
						break

			print (f"+++ Empresa no autorizada...")
			raise IllegalEmpresaException (f"NETERROR::Empresa no autorizada: '{empresa}'.\\\\Verifique si está autorizado e inicie nuevamente.")

		except (TransportError, httplib2.ServerNotFoundError, socket.gaierror) as ex:
			print (f"NETERROR::Connection issue: {ex}")
			errorsList.append (EcuerrorNetworkConnection ("NETERROR::Problemas de conexión internet.\\\\Verifique su conexión a Internet e inicie nuevamente."))
			raise
		except HttpError as ex:
			print (f"NETERROR::Google API issue: {ex}")
			errorsList.append (EcuerrorNetworkConnection ("NETERROR::Problemas de conexión con Google.\\\\Verifique si está autorizado e inicie nuevamente."))
			raise

		except EcudocException as ex:
			errorsList.append (ex)
			raise

		except Exception as ex:
			print (f"NETERROR::General authorization issue : {ex}")
			errorsList.append (EcudocCloudException (f"CLOUDERROR::Problemas verificando autorización de la empresa: '{empresa}'"))
			raise

	#----------------------------------------------------------------
	# Check in background if empresa is authorized or not. Raises an event
	#----------------------------------------------------------------
	def verifyAuthorizedEmpresa (empresa):
		Utils.log ("Verifying authorized empresa")
		try:
			credentials = EcuCloud.getGoogleCredentials ()
			sheet       = EcuCloud.getGoogleSheet ('clients', credentials)
			records     = sheet.get_all_records()
			for record in records:
				if record.get ("EMPRESA") == empresa:
					if record.get("AUTORIZACION", "").strip().upper() == "SI":
						Utils.log (f"+++++++++++++++ Empresa '{empresa}' está autorizada ++++++++++++++++")
						return True
					else:
						break

			Utils.log (f"+++ Empresa no autorizada...")
			raise IllegalEmpresaException (f"NETERROR::Empresa no autorizada: '{empresa}'.\\\\Verifique si está autorizado e inicie nuevamente.")

		except (TransportError, httplib2.ServerNotFoundError, socket.gaierror) as ex:
			print (f"NETERROR::Connection issue: {ex}")
			raise
		except HttpError as ex:
			print (f"NETERROR::Google API issue: {ex}")
			raise
		except EcudocException as ex:
			raise
		except Exception as ex:
			print (f"NETERROR::General authorization issue : {ex}")
			raise


	def runEventAuthorizedEmpresa (empresa):
		Utils.log ("Running runEventAuthorizedEmpresa...")
		EcuCloud.authorizedEmpresaDone.clear () # reset event
		def worker ():
			try:
				EcuCloud.verifyAuthorizedEmpresa (empresa)
				EcuCloud.authorizedEmpresaError = None
			except Exception as ex:
				Utils.log (str (ex))
				EcuCloud.authorizedEmpresaError = ex
			finally:
				EcuCloud.authorizedEmpresaDone.set()  # signal completion

		thread = threading.Thread (target=worker)
		thread.start ()
		return thread

	def checkEventAuthorizedEmpresa ():
		if EcuCloud.authorizedEmpresaDone.wait (timeout=5):
			if EcuCloud.authorizedEmpresaError:
				raise authorizedEmpresaError
			else:
				print (f"+++ Verificación empresa autorizada finalizado con éxito")
				return True
		else:
			raise IllegalEmpresaException (f"NETERROR::Tiempo expirado verificando autorización de empresa.\\\\Verifique si está autorizado e inicie nuevamente.")




	#----------------------------------------------------------------
	# Send transportista info
	#----------------------------------------------------------------
	def logTransportistaInfo (empresa, nombre, direccion):
		try:
			credentials                = EcuCloud.getGoogleCredentials ()
			sheet                      = EcuCloud.getGoogleSheet ('transportista', credentials)
			timestamp                  = EcuCloud.getCurrentDateTimeString ()
			sheet.append_row ([empresa, nombre, direccion])
		except:
			Utils.printException (f"Error enviando log transportista: '{empresa}', '{nombre}', '{direccion}'")
			Utils.printx (traceback.format_exc())

	#----------------------------------------------------------------
	#----------------------------------------------------------------
	def getCurrentDateTimeString ():
		current_datetime = datetime.now()
		#formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H:%M:%S")
		#formatted_datetime = current_datetime.strftime("%Y%m%d:%H%M%S")
		formatted_datetime = current_datetime.strftime("%Y%m%d:%H%M")
		return formatted_datetime

	#----------------------------------------------------------------
	# Get access key from cloud. (e.g. SANCHEZPOLO::SPL112050
	#----------------------------------------------------------------
	def getAccessKey (empresa):
		try:
			sheet         = EcuCloud.getGoogleSheet ('accesskeys', credentials)
			accessKeyList = sheet.col_values (1)  # Assuming usernames are in the first column

			for accessKey in accessKeyList:
				if empresa in accessKey:
					key = accessKey.split ("::")[1]
					return key
			return None
		except Exception as ex:
			raise EcudocCloudException (f"CLOUDERROR::No se pudo validar clave de acceso en la Web")

	#----------------------------------------------------------------
	# Get install key from cloud. (e.g. SANCHEZPOLO::SPL112050
	#----------------------------------------------------------------
	def getInstallKey (empresa):
		try:
			credentials   = EcuCloud.getGoogleCredentials ()
			sheet         = EcuCloud.getGoogleSheet ('installkeys', credentials)
			clientKeyList = sheet.col_values (1)  # Assuming usernames are in the first column

			for clientKey in clientKeyList:
				if empresa in clientKey:
					key = clientKey.split ("::")[1]
					return key
			return None
		except Exception as ex:
			raise EcudocCloudException (f"CLOUDERROR::No se pudo validar clave de instalación en la Web")

	#----------------------------------------------------------------
	#----------------------------------------------------------------
	def validate_user (username):
		clientNames = EcuCloud.get_valid_usernames()
		if username in clientNames:
			return True
		else:
			return False

	#----------------------------------------------------------------
	#----------------------------------------------------------------
	def get_valid_usernames ():
		sheet       = EcuCloud.getGoogleSheet ('clients', credentials)
		clientNames = sheet.col_values (1)  # Assuming usernames are in the first column
		print (f"+++ clients '{clientNames}'")
		return clientNames


	#----------------------------------------------------------------
	#----------------------------------------------------------------
	def getDecodedString ():
		# Step 1: Decode the Base64 string
		decoded_bytes = base64.b64decode (EcuCloud.googleKeyString)
		decoded_str   = decoded_bytes.decode('utf-8')
		# Step 2: Parse the JSON string
		jsonString    = json.loads (decoded_str)
		return jsonString

	#---------------------------------------------------------------------
	# Check/download for new patch in github releases.
	# Check if the patch hasn't been applied in "patches.log".
	#---------------------------------------------------------------------
	@classmethod
	def checkDowloadPatchFromGit (cls):
		API_URL  = f"https://api.github.com/repos/{cls.GITUSER}/{cls.GITREPO}/releases/latest"
		#---------------- Local Functions --------------------------------
		def getVersion (patchName):
			patchVersion = patchName.split ("_")[1].split (".")[0]
			return patchVersion

		def getLastAppliedPatch (logPatchesFilename):
			patchName = None
			try:
				if os.path.exists (logPatchesFilename):
					patchLine = open (logPatchesFilename).readlines ()[0]
					patchName = patchLine.strip ()
			except Exception as ex:
				Utils.printException ("No se pudo abrir el archivo de logs de actualizaciones (patches)")
			return patchName

		def downloadPatch (patch_asset, patch_name, outputDir):
			download_url = patch_asset ["browser_download_url"]
			outFilename  = os.path.join ("patches", patch_name)

			print(f"Downloading update: {patch_name} from {download_url}")
			with requests.get (download_url, stream=True) as r:
				r.raise_for_status()
				with open (outFilename, "wb") as f:
					for chunk in r.iter_content(chunk_size=8192):
						f.write(chunk)

			print (f"Download complete: {patch_name}")
		#-----------------------------------------------------------------
		try:
			print(f"Checking for updates from {API_URL}...")
			response = requests.get(API_URL)
			response.raise_for_status()
			release = response.json()

			# Search assets for your installer
			patch_asset = None
			for asset in release ["assets"]:
				if asset["name"].lower().endswith((".vcdiff")):
					patch_asset = asset
					break

			if not patch_asset:
				print("No installer asset found in the latest release.")
				return False
				
			lastAppliedPatch = getLastAppliedPatch (cls.PATCHESLOG)
			patch_name       = patch_asset ["name"]
			if lastAppliedPatch and getVersion (patch_name) <= getVersion (lastAppliedPatch):
				print ("Latest patch is already applied:", lastAppliedPatch, "vs", patch_name)
				return False

			downloadPatch (patch_asset, patch_name, "patches")
			print ("Restart to run autoupdate")
			return True
		except requests.RequestException as e:
			print(f"Error checking for updates: {e}")
			return False

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main()

