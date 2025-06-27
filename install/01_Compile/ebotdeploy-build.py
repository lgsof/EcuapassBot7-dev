#!/usr/bin/env python3
"""
Create pyinstall dir with .pyc files and resources to
create the .exe using the .pyc files
"""

import os, sys
from os.path import join
import shutil as sh, glob

#----------------------------------------------------------
#----------------------------------------------------------
exeDir      = 'winexe'
RX          = None    # {RX} or rmdir
pycCompiler = 'python -m compileall -l %s'
pyaCompiler = 'pyarmor gen --output dist/obfuscated %s'

#compilerStr = pycCompiler
compilerStr = pycCompiler

if sys.platform == 'linux':
	PATH = '/home/lg/BIO/ecuapassdocs/EcuapassBot7/EcuapassBot7-dev/commander'
	RX   = 'rx'
else:
	PATH = 'Z:\\bot7\\commander'
	RX   = 'rmdir /S/Q'

def main ():
	if os.path.exists (exeDir):
		sh.rmtree (exeDir)

	os.makedirs (exeDir)
	print ('Copy main files...')
	sh.copy (f"ebotdeploy-pyinstaller.spec", exeDir)
	sh.copy (f"admin.manifest", exeDir)
	sh.copy (join (PATH, 'ecuapass_commander.py'), exeDir)

	os.chdir (exeDir)

	print ('Compiling commander...')
	cacheDir = join (PATH, '__pycache__')
	os.system (f'{RX} {cacheDir}')
	cmm = compilerStr % PATH
	print ("+++  ", cmm)
	os.system (compilerStr % PATH)
	copyFiles (cacheDir, ".", "pyc")

	print ('Compiling scraping...')
	cacheDir = join (PATH, "scraping", '__pycache__')
	os.system (f'{RX} {cacheDir}')
	os.system (compilerStr % join (PATH, "scraping"))
	copyFiles (cacheDir, "scraping", "pyc")


	print ('Compiling info...')
	cacheDir = join (PATH, "info", '__pycache__')
	os.system (f'{RX} {cacheDir}')
	os.system (compilerStr % join (PATH, "info"))
	copyFiles (cacheDir, "info", "pyc")

	# Resources
	print ('Copying resource data_ecuapass files...')
	resDir = join ('resources','data_ecuapass')
	copyFiles (join (PATH, resDir), resDir, 'txt')

	print ('Copying resource docs files...')
	resDir = join ('resources','docs')
	srcDir = join (PATH, resDir)
	copyFiles (srcDir, resDir, 'json')
	copyFiles (srcDir, resDir, 'png')
	copyFiles (srcDir, resDir, 'pdf')

	print ('Copying resource image files...')
	imgDir = join ('resources','images')
	copyFiles (join (PATH, imgDir), imgDir, 'png')
	copyFiles (join (PATH, imgDir), imgDir, 'DIR')

#----------------------------------------------------------
# Move python cache files '.pyc' from cache to current dir
#----------------------------------------------------------
def copyFiles (inputDir, destDir, fileType):
	os.makedirs (destDir, exist_ok=True)
	for file in os.listdir (inputDir):
		inputFile = os.path.join (inputDir, file)
		try:
			if file.endswith (".pyc"):
				# Extract the module name
				module_name = file.split (".")[0] + ".pyc"
				outputFile = os.path.join (destDir, module_name)
			else:
				outputFile = os.path.join (destDir, file)

			print (f'Copying file "{inputFile}" to  {outputFile}...')
			if fileType == 'DIR' and os.path.isdir (inputFile): 
				sh.copytree (inputFile, outputFile)
			elif file.endswith (fileType):
				sh.copy (inputFile, outputFile)
		except Exception as ex:
			print (f'Error Copying file "{inputFile}" to  {outputFile}...')
			print (str(ex))
			sys.exit (0)

		# Remove the __pycache__ directory
		#sh.rmtree (cache_dir)
#----------------------------------------------------------
#----------------------------------------------------------
main ()
