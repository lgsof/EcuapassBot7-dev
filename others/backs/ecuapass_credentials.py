#!/usr/bin/env python3

"""
Class for handle binary credentials by "empresa": 
	- Codebin pais:user:password
	- Azure connection string
"""
import os, sys, base64, pickle, json
USAGE="""\n
ecuapass_settings.py [--print|--textToBin|--binToText] <filename>
\n"""

def main ():
	args = sys.argv
	if len (args) < 2:
		print (USAGE)
		sys.exit (0)

	option	   = args [1]
	filename   = args [2]
	runningDir = os.getcwd ()
	credentials   = EcuCredentials ()

	if option == "--print":
		print ("+++ print binary credentials")
		credentials.printCredentials (filename)
	elif option == "--textToBin":
		print ("+++ Text to bin")
		binFilename = filename.rsplit (".", 1)[0] + ".bin"
		credentials.textToBin (filename, binFilename)
	elif option == "--binToText":
		print ("+++ Bin to text")
		txtFilename = filename.rsplit (".", 1)[0] + ".txt"
		credentials.binToText (filename, txtFilename)
	else:
		print (f"Option '{option}' not known")


class EcuCredentials:
	def __init__ (self, settingsFile="settings.bin"):
		self.runningDir = os.getcwd ()     # Credentials must be in the initial working dir
		self.settingsFilepath = os.path.join (self.runningDir, settingsFile)

	#------------------------------------------------------
	#-- Print settins opened from bin file
	#------------------------------------------------------
	def printCredentials (self, settingsFilepath):
		self.settingsFilepath = settingsFilepath
		credentials = self.readBinCredentials ()
		for k,v in credentials.items():
			print (f"{k} : {v}")
	#------------------------------------------------------
	#------------------------------------------------------
	def readBinCredentials (self, binFilename=None):
		""" Get JSON from binary file
		"""
		if not binFilename:
			binFilename = self.settingsFilepath
		with open (binFilename, 'rb') as binary_file:
			base64_dict = binary_file.read ()

		decoded_bytes = base64.b64decode (base64_dict)
		json_string   = decoded_bytes.decode ('utf-8')
		dictionary    = json.loads(json_string)

		return dictionary

	#------------------------------------------------------
	#------------------------------------------------------
	def getParameter (self, parameterName):
		""" Get parameter from credentials dictionary
		"""
		dictionary = self.readBinCredentials ()
		value = dictionary [parameterName]
		return value

	#------------------------------------------------------
	#------------------------------------------------------
	def textToBin (self, text_filename, binFilename):
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
	def binToText (self, binFilename, text_filename):
		""" Create binary file from JSON file
		"""
		dictionary = self.readBinCredentials (binFilename)

		# Write to text file
		with open (text_filename, 'w') as text_file:
			json.dump (dictionary, text_file, indent=4)

		return dictionary

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()
