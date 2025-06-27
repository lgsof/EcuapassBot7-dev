#!/usr/bin/env python3

import sys, json


def copyAldiaFieldsFromParamsToParams (paramsFilename01, paramsFilename02):
	params01 = json.load (open (paramsFilename01))
	params02 = json.load (open (paramsFilename02))

	for k in params01:
		try:
			v2 = params02 [k]
			params01 [k]["aldiaField"] = v2 ["aldiaField"]
		except:
			print (f"+++ Exception in key '{k}'")
	
	outFile = paramsFilename01.split (".")[0] + "-new.json"
	json.dump (params01, open (outFile, "w"), indent=4)



args = sys.argv
paramsFilename01 = args [1]
paramsFilename02 = args [2]
copyAldiaFieldsFromParamsToParams (paramsFilename01, paramsFilename02)
