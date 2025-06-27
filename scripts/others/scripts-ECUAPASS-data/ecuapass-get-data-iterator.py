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
py.sleep (5)
oldText = ""
i=0
while True:
	py.press ("end")
	for k in range (0, i):
		py.press ("up"); py.sleep (0.01)

	py.hotkey ("ctrl", "a", "c"); py.sleep (0.01)
	text = pyperclip_paste()
	print ("TEXT:", text)
	open ("data.txt", "a").write (text + "\n")
	py.press ("enter"); py.sleep (0.01)

	i += 1

	if text == oldText:
		break
	else:
		oldText = text


