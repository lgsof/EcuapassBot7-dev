#!/usr/bin/env python3
"""
Create settings for each empresa
"""
import os, sys

if sys.platform == 'linux':
	path  = '/home/lg/BIO/ecuapassdocs/EcuapassBot/EcuapassBot6-dev/settings/'
	cpCmm = "cp"
else:
	path = 'Z:\\bot6\\settings\\'
	cpCmm = "copy"


args = sys.argv

empresa = args [1]
empresa = empresa.upper ()

cmm = f"{cpCmm} {path}settings-{empresa}.bin settings.bin"
print ('+++', cmm)
os.system (cmm)

