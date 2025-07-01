#!/usr/bin/env python3

import requests
import sys
import os

USER     = "lgsof"
REPO     = "EcuapassBot7-win"
API_URL  = f"https://api.github.com/repos/{USER}/{REPO}/releases/latest"
LOGSFILE = "patches/patches.log"

#---------------------------------------------------------------------
#---------------------------------------------------------------------
def main ():
	checkDowloadPatch ()

#---------------------------------------------------------------------
#---------------------------------------------------------------------
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
		print (ex)
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

#---------------------------------------------------------------------
#---------------------------------------------------------------------
def checkDowloadPatch ():
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
			
		lastAppliedPatch = getLastAppliedPatch (LOGSFILE)
		patch_name       = patch_asset ["name"]
		if lastAppliedPatch and getVersion (patch_name) <= getVersion (lastAppliedPatch):
			print ("Lates patch is already applied:", lastAppliedPatch, "vs", patch_name)
			return False

		downloadPatch (patch_asset, patch_name, "patches")
		print ("Restart to run autoupdate")
		return True
	except requests.RequestException as e:
		print(f"Error checking for updates: {e}")
		return False

#---------------------------------------------------------------------
#---------------------------------------------------------------------
main ()
