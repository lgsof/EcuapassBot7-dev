#!/usr/bin/env python3
"""
Get information from Ecuapass data fields by selecting, copying, down
"""


import time, re
import pyautogui as py

import pyperclip
from pyperclip import copy as pyperclip_copy
from pyperclip import paste as pyperclip_paste


dataFile = open ("data.txt", "w")
input ("Aliste cursor en ECUAPASS field...")
py.sleep (3)
oldText = ""
while True:
	py.hotkey ("ctrl", "a", "c"); py.sleep (0.1)
	py.press ("enter"); py.sleep (0.1)
	text = pyperclip_paste()
	print ("TEXT:", text)
	dataFile.write (text + "\n")

	value = text
	if not "Selecc" in text and text!="":
		#value = text.split (" ", 1)[1]
		value = re.match (r"^\[(.*?)\]", text).group(1)

	pyperclip_copy (value)
	py.hotkey ("ctrl", "v")
	py.press ("down"); py.sleep (0.1)
	py.press ("enter"); py.sleep (0.1)
	py.press ("down"); py.sleep (0.1)
	
	if text == oldText:
		break
	else:
		oldText = text

