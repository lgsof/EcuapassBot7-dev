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
exeDir  = 'winexe'
PATH    = '/home/lg/BIO/ecuapassdocs/EcuapassBot/EcuapassBot6-dev/ecuserver'
def main ():
	createExeDir ()
	sh.copy ("ecuapass_commander-LG.spec", exeDir)

#----------------------------------------------------------
#----------------------------------------------------------
def createExeDir ():
	print ('Creating exe dir...')
	if os.path.exists (exeDir):
		sh.rmtree (exeDir)

	print ('Copy main py file...')
	sh.copy (f'{PATH}/ecuapass_commander.py', exeDir)

	print ('Compile all...')
	cmm = f'python -m compileall -l {PATH}'
	print ('+++', cmm)
	os.system (cmm)

	print ('Copying main cache files to exe dir...')
	copyFiles (f"{PATH}/__pycache__", "winexe", "pyc")

	print ('Creating winexe/ecuapassdocs...')
	infoDir = join (PATH, 'ecuapassdocs', 'info')

	print ('Compiling info...')
	cmm = f'python -m compileall -l {infoDir}'
	print ('+++', cmm)
	os.system (cmm)

	print ('Copying info cache files to exe dir...')
	infoDirCache = join (infoDir, '__pycache__')
	copyFiles (infoDirCache, join (exeDir, infoDir), "pyc")

	print ('Copying resource data_ecuapass files...')
	resDir = join (PATH, 'ecuapassdocs','resources','data_ecuapass')
	copyFiles (resDir, join (exeDir, resDir), 'txt')

	print ('Copying resource docs files...')
	resDir = join (PATH, 'ecuapassdocs','resources','docs')
	copyFiles (resDir, join (exeDir, resDir), 'json')
	copyFiles (resDir, join (exeDir, resDir), 'png')
	copyFiles (resDir, join (exeDir, resDir), 'pdf')

	print ('Copying resource image files...')
	resDir = join (PATH, 'ecuapassdocs','resources','images')
	copyFiles (resDir, join (exeDir, resDir), 'png')

#----------------------------------------------------------
# Move python cache files '.pyc' from cache to current dir
#----------------------------------------------------------
def copyFiles (inputDir, destDir, fileType):
	os.makedirs (destDir, exist_ok=True)
	for file in [x for x in os.listdir (inputDir) if x.endswith (f".{fileType}")]:
		inputFile, outputFile = '',''
		try:
			if file.endswith (".pyc"):
				# Extract the module name
				module_name = file.split (".")[0] + ".pyc"
				inputFile  = os.path.join (inputDir, file)
				outputFile = os.path.join (destDir, module_name)
			else:
				inputFile  = os.path.join (inputDir, file)
				outputFile = os.path.join (destDir, file)

			print (f'Copying file "{inputFile}" to  {outputFile}...')
			sh.copy (inputFile, outputFile)
		except:
			print (f'Error Moving file "{inputFile}" to  {outputFile}...')

		# Remove the __pycache__ directory
		#sh.rmtree (cache_dir)
#----------------------------------------------------------
#----------------------------------------------------------
main ()
