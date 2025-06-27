#!/usr/bin/env python3

"""
Class for handle binary Settings by "empresa": 
	- Codebin pais:user:password
"""

import os, sys, base64, pickle, json

try:
	from info.ecuapass_utils import Utils
	from info.ecuapass_extractor import Extractor
except:
	pass

USAGE="""\n
ecuapass_settings.py [--print|--textToBin|--binToText] <filename>
\n"""

#--------------------------------------------------------------------
# main
#--------------------------------------------------------------------
def main ():
	args = sys.argv
	if len (args) < 2:
		print (USAGE)
		sys.exit (0)

	option, filename, runningDir = args [1], args [2], os.getcwd ()

	if option == "--print":
		print ("+++ print binary Settings")
		Settings.printSettings (filename)
	elif option == "--textToBin":
		print ("+++ Text to bin")
		binFilename = filename.rsplit (".", 1)[0] + ".bin"
		Settings.textToBin (filename, binFilename)
	elif option == "--binToText":
		print ("+++ Bin to text")
		txtFilename = filename.rsplit (".", 1)[0] + ".txt"
		Settings.binToText (filename, txtFilename)
	else:
		print (f"Option '{option}' not known")

#--------------------------------------------------------------------
# Handle 'Empresa' settings: data, credentidals, globals
#--------------------------------------------------------------------
class Settings:
	empresa           = None
	version           = None
	settingsFilepath  = None

	# Settings saved in file
	configData        = None
	configCPI         = None
	configMCI         = None

	@classmethod
	def init (cls, empresa, version, runningDir, settingsFile="settings.bin"):
		cls.empresa          = empresa
		cls.version          = version
		cls.runningDir       = runningDir
		cls.settingsFilepath = os.path.join (runningDir, settingsFile)

	#------------------------------------------------------------------
	# Check if "empresa" has a URL of the documents website
	# Not checked if it the URL is valid or not
	#------------------------------------------------------------------
	@classmethod
	def hasCodebinWebAccess (cls):
		if cls.configData ["appType"] == "COREBD" and cls.configData ["urlWebsite"].strip():
			return True
		return False

	#------------------------------------------------------------------
	# Return PDF coordinates file
	#------------------------------------------------------------------
	@classmethod
	def getCoordinatesFile (cls):
		return cls.configData ["coordsFile"]

	#------------------------------------------------------------------
	#-- Check if token is contained in text
	#------------------------------------------------------------------
	@classmethod
	def checkEmpresaToken (cls, tokenText):
		from info.ecuapass_exceptions import IllegalEmpresaException
		tokenString = cls.configData ["token"]
		tokens		= tokenString.split ("|") # if more than one token
		print (f"+++ tokenText '{tokenText}'")
		for tk in tokens:
			print (f"+++ token '{tk}'")

			if tk in tokenText:
				return cls.configData ["id"]

		raise IllegalEmpresaException (f"PDFERROR::Token no reconocido en empresa: '{cls.empresa}'")
	
	#----------------------------------------------------------------
	# Check if is a valid 'empresa' by validating 'permiso'
	#----------------------------------------------------------------
	@classmethod
	def checkEmpresaPermisos (cls, permisoText):
		from info.ecuapass_exceptions import IllegalEmpresaException
		from info.ecuapass_utils import Utils
		permisoEmpresa = None
		try:
			permisoEmpresa = cls.configData ["permiso"]
			permisosList   = permisoEmpresa.split ("|")
			for p in permisosList:
				permiso     = Utils.removeSymbols (p)
				permisoText = Utils.removeSymbols (permisoText)

				if permiso and permiso in permisoText:
					return permisoEmpresa

			raise IllegalEmpresaException (f"SCRAPERROR::Empresa no reconocida. Problemas de permisos.")

		except IllegalEmpresaException:
			Utils.printException ('SCRAPERROR::Empresa no reconocida:', cls.empresa)
			raise
		except Exception as ex:
			Utils.printException ('Problemas validando la empresa:', cls.empresa)
			raise IllegalEmpresaException (f"SCRAPERROR::Problemas validando empresa: '{empresa}'!") from ex


	#------------------------------------------------------
	#---------------- Parameters --------------------------
	#------------------------------------------------------
	# Get a key from ConfigPanel
	#------------------------------------------------------
	@classmethod
	def get (cls, keyType, key):
		try:
			if keyType == "DATA":
				return cls.configData [key].strip()
			elif keyType == "CPI":
				return cls.configCPI [key].strip()
			elif keyType == "MCI":
				return cls.configMCI [key].strip()
			else:
				raise Exception ("No existe llave:", key)
		except Exception as ex:
			from info.ecuapass_utils import Utils
			Utils.printException (f"Error obteniendo valor desde '{keyType}' : '{key}'")
			return ""

	#------------------------------------------------------
	# Get "Dias Entrega" from Cartaporte Config
	#------------------------------------------------------
	@classmethod
	def getDiasEntrega (cls, diasEntrega): # Default days
		from info.ecuapass_utils import Utils
		try:
			dias = cls.get ("CPI", "08_Entrega")
			if dias:
				diasEntrega = int (dias.split ("|")[0])
		except Exception as ex:
			Utils.printException ("Error configuración Cartaporte::dias de entrega")
		return diasEntrega

	#------------------------------------------------------
	# Get description text: 1 line, 1 paragraph, ALL
	#------------------------------------------------------
	@classmethod
	def getDescripcion (cls, descripcion, params):
		try:
			if params.lower().strip() == "1_linea":
				return Extractor.getFirstLine (descripcion)
			elif params.lower().strip() == "1_parrafo":
				return Extractor.getFirstParagraph (descripcion)
			elif "SEPARADOR" in params.upper().strip():
				sep = params.split("=")[1]
				return descripcion.split (sep)[0]
		except:
			Utils.printException ("Error configuración Cartaporte::Descripcion")
		return descripcion

	#------------------------------------------------------
	# Get path were files are saved
	#------------------------------------------------------
	def getDocumentsPath ():
		relative_path = os.path.join("Documents", "Ecuapassdocs")
		absolute_path = os.path.join(os.path.expanduser("~"), relative_path)
		return os.path.normpath (absolute_path)
	
	#------------------------------------------------------
	#-- Print settins opened from bin file
	#------------------------------------------------------
	@classmethod
	def printSettings (cls, settingsFilepath):
		cls.settingsFilepath = settingsFilepath
		Settings = cls.readBinSettings ()
		for k,v in Settings.items():
			print (f"{k} : {v}")

	#------------------------------------------------------
	#------------------------------------------------------
	@classmethod
	def readBinSettings (cls, binFilename=None):
		""" Get JSON from binary file
		"""
		if not binFilename:
			binFilename = cls.settingsFilepath
		with open (binFilename, 'rb') as binary_file:
			base64_dict = binary_file.read ()

		decoded_bytes  = base64.b64decode (base64_dict)
		json_string    = decoded_bytes.decode ('utf-8')
		settings = json.loads(json_string)
		cls.configData = settings ["datos"]
		cls.configCPI  = settings ["cartaporte"]
		cls.configMCI  = settings ["manifiesto"]

		return settings

	#------------------------------------------------------
	#------------------------------------------------------
	@classmethod
	def reload (cls):
		return cls.readBinSettings ()
	
	#------------------------------------------------------
	#------------------------------------------------------
	@classmethod
	def getParameter (cls, parameterName):
		""" Get parameter from Settings dictionary
		"""
		dictionary = cls.readBinSettings ()
		value = dictionary [parameterName]
		return value

	#------------------------------------------------------
	#------------------------------------------------------
	@classmethod
	def textToBin (cls, text_filename, binFilename):
		""" Reads a dictionary from a text file and writes it to a binary file.
		"""
		with open(text_filename, 'r') as text_file:
			dictionary = eval (text_file.read())

		# Convert the dictionary to a JSON string
		json_string = json.dumps (dictionary)
		# Encode the JSON string to bytes with UTF-8 encoding
		encoded_bytes = json_string.encode('utf-8')		
		# Serialize the dictionary and encode it in base64
		base64_encoded_dict = base64.b64encode (encoded_bytes)

		with open(binFilename, 'wb') as binary_file:
			binary_file.write (base64_encoded_dict)

	#------------------------------------------------------
	#------------------------------------------------------
	@classmethod
	def binToText (cls, binFilename, text_filename):
		""" Create binary file from JSON file
		"""
		dictionary = cls.readBinSettings (binFilename)

		# Write to text file
		with open (text_filename, 'w') as text_file:
			json.dump (dictionary, text_file, indent=4)

		return dictionary

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()
