#!/usr/bin/env python3
"""
Add 13px to items from txt34 to the end
This is necesary for ALDIA : ECUADOR : MANIFIESTOS
"""


import sys, json

args = sys.argv

jsonFilename = args [1]

data = json.load (open (jsonFilename))
manifiesto = data ["MANIFIESTO"]
keys = ["32_2","32_4","33_2","34","35","36","37","38","39","40"]
for k in keys:
	id = f"txt{k}"
	v = manifiesto [id]
	try:
		print (f"\nORG: k:{k}: {v}")
		org_y = int (v [1])
		new_y = org_y + 13
		v [1] = new_y
		print (f"NEW: k:{k}: {v}")
		manifiesto [k] = v
	except:
		print (f"--- {k}")

data ["MANIFIESTO"] = manifiesto

newJsonFilename = jsonFilename.split (".")[0] + "-new.json"
json.dump (data, open (newJsonFilename, "w"), indent=4)
