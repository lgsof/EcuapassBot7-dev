#!/usr/bin/env python3

VERSION="0.970"
"""
LOG: 
Nov/29 : 0.964 : Working for SANCHEZPOLO. Working ScrapingWeb.
"""

import os, sys, time

# For ecuapassdocs functions
from info.ecuapass_utils import Utils

# doc, document bots
from ecuapass_doc import EcuDoc

#----------------------------------------------------------------
# Listen for remote calls from Java GUI
# Called with the running dir as unique argument
#----------------------------------------------------------------
def main ():
	# Notify the caller (Java) that the process is ready
#	args = sys.argv

	print ("Python executable is ready to receive commands.", flush=True)

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()
