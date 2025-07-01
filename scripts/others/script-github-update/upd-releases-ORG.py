#!/usr/bin/env python3

import requests
import sys
import os

USER = "lgsof"
REPO = "EcuapassBot7-win"
CURRENT_VERSION = "v0.8.9"	# your current app version

API_URL = f"https://api.github.com/repos/{USER}/{REPO}/releases/latest"

try:
	print(f"Checking for updates from {API_URL}...")
	response = requests.get(API_URL)
	response.raise_for_status()
	release = response.json()

	latest_version = release["tag_name"]
	print(f"Latest version on GitHub: {latest_version}")

	if latest_version > CURRENT_VERSION:
		print(f"New version available: {latest_version} (current: {CURRENT_VERSION})")

		# Search assets for your installer
		installer_asset = None
		for asset in release["assets"]:
			print (f"+++ asset: '{asset}'")
			if asset["name"].lower().endswith((".vcdiff")):
				installer_asset = asset
				break

		if installer_asset:
			download_url = installer_asset["browser_download_url"]
			filename = installer_asset["name"]

			print(f"Downloading update: {filename} from {download_url}")
			with requests.get(download_url, stream=True) as r:
				r.raise_for_status()
				with open(filename, "wb") as f:
					for chunk in r.iter_content(chunk_size=8192):
						f.write(chunk)

			print(f"Download complete: {filename}")
			print("You can now run the installer or apply the update.")
		else:
			print("No installer asset found in the latest release.")
	else:
		print("You already have the latest version.")

except requests.RequestException as e:
	print(f"Error checking for updates: {e}")
	sys.exit(1)

