#!/usr/bin/env python3

"""
Convert file text to vertical lines or horizontal string
"""

import sys

def main ():
	args = sys.argv

	if len (args) > 1:
		option = args [1]
		if option == "--hrzToVrt":
			connStringFilename = args [2]
			connStringToVertical (connStringFilename)
		elif option == "--vrtToHrz":
			connStringFilename = args [2]
			connStringToHorizontal (connStringFilename)

def connStringToVertical (connStringFilename):
	#print ("+++ To Vertical")
	connString = open (connStringFilename).read()
	for char in connString:
		print (char)

def connStringToHorizontal (connStringFilename):
	#print ("+++ To Horizontal")
	connStringLines = open (connStringFilename).readlines()
	connString = "".join ([x.replace ("\n","") for x in connStringLines])
	print (connString)

main ()
