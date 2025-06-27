import re, os, sys, json, datetime
"""
Main Bot for typing Cartaportes and Manifiestos to ECUAPASS
"""

import pyautogui as py
from pyautogui import ImageNotFoundException

import pywinauto

from pyperclip import copy as pyperclip_copy
from pyperclip import paste as pyperclip_paste

from info.ecuapass_utils           import Utils
from info.ecuapass_info_cartaporte import CartaporteInfo
from info.ecuapass_info_manifiesto import ManifiestoInfo
from info.ecuapass_exceptions      import EcudocEcuapassException, EcuerrorImageNotFound
from info.ecuapass_exceptions      import EcudocBotStopException, EcudocTypingError
from info.ecuapass_extractor       import Extractor

#----------------------------------------------------------
# Avoid pyautogui FAILSAFE. Alternative: control dialog stop button
#----------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')
py.FAILSAFE = False  # Disable failsafe globally

#----------------------------------------------------------
# General Bot class with basic functions of auto completing
#----------------------------------------------------------
class EcuBot:
	#-- Load data, check/clear browser page
	def __init__ (self, empresa, ecuFieldsFilepath, runningDir, docType):
		self.empresa          = empresa
		self.runningDir       = runningDir	   
		self.docType	      = docType
		self.fields           = json.load (open (ecuFieldsFilepath, encoding="utf-8"))
		self.mouseController  = None   # Initialized for child objects


		self.ecuapassWinTitle = 'ECUAPASS - SENAE browser'
		Utils.runningDir      = runningDir

		self.NORMAL_PAUSE     = 0.05     # float (settings ["NORMAL_PAUSE"])
		self.SLOW_PAUSE       = 0.5      # float (settings ["SLOW_PAUSE"])
		self.FAST_PAUSE       = 0.01     # float (settings ["FAST_PAUSE"])
		py.PAUSE		      = self.NORMAL_PAUSE

	#-------------------------------------------------------------------
	# Create Cartaporte/Manifiesto Bot
	#-------------------------------------------------------------------
	def createBot_OBJECT (empresa, ecuFieldsFilepath, runningDir, coordinatesString):
		from mouse_controller import MouseController
		docType = Utils.getDocumentTypeFromFilename (ecuFieldsFilepath)

		if docType == "CARTAPORTE":
			from ecuapass_bot_cartaporte import EcuBotCartaporte
			bot = EcuBotCartaporte (empresa, ecuFieldsFilepath, runningDir)
		elif docType == "MANIFIESTO":
			from ecuapass_bot_manifiesto import EcuBotManifiesto
			bot = EcuBotManifiesto (empresa, ecuFieldsFilepath, runningDir)
		else:
			raise Exception (f"ERROR: Tipo documento desconocido: '{os.path.basename (ecuFieldsFilepath)}'")

		# Create mouseController to confine/release mouse in scrollN
		bot.mouseController  = MouseController (coordinatesString)

		return bot

	#-- Detect and activate ECUAPASS-browser/ECUAPASS-DOCS window
	def activateEcuapassWindow (self):
		try:
			Utils.printx ("Activando la ventana del ECUAPASS...")

			# Connect to an existing instance of an application by its title
			app             = pywinauto.Application().connect (title=self.ecuapassWinTitle)
			ecuapass_window = app.window (title=self.ecuapassWinTitle)
			py.sleep (0.1)
			ecuapass_window.set_focus()
			py.sleep (0.2)

			# Detect and clear webpage
			#EcuBot.scrollWindowToBeginning ()
			#self.waitForInfo ()

			return ecuapass_window
		except pywinauto.ElementNotFoundError:
			raise EcudocEcuapassException (f"BOTERROR::No está abierta la ventana del ECUAPASS")

	#--------------------------------------------------------------------
	# Detect if is on find button using image icon
	#--------------------------------------------------------------------
	def isOnFindButton (self):
		try:
			Utils.printx ("Localizando botón de búsqueda...")
			xy = EcuBot.findEcuapassImage ("image-button-FindRUC", 0.90)
			return True
		except ImageNotFoundException as ex:
			print ("Imágen de botón de búsqueda no encontrado")
			return False
	#--------------------------------------------------------------------
	# Find image in Ecuapass website probing multiple images in a dir
	#--------------------------------------------------------------------
	def findEcuapassImage (imageDirname, CONFIDENCE=0.80):
		filePaths = Utils.getPathImage (imageDirname)
		for fpath in filePaths:
			try:
				print ("\t>>> Buscando: ", fpath)
				xy = py.locateCenterOnScreen (fpath, confidence=CONFIDENCE, grayscale=True)
				Utils.printx ("\t>>> Encontrada!!!")
				return xy
			except ImageNotFoundException as ex:
				print (f"\\>>> Intento fallido")
		raise ImageNotFoundException (f"Imágen '{fpath}' no encontrada")

	#--------------------------------------------------------------------
	# Fill one of three radio buttons (PO, CI, PEOTP) according to input info
	#--------------------------------------------------------------------
	def fillRButton (self, fieldName):
		value = self.fields [fieldName]
		if (value == "1"):
			py.press ("Tab")
		else:
			py.press ("right")

	#--------------------------------------------------------------------
	#-- fill text field
	#--------------------------------------------------------------------
	def fillText (self, fieldName, TAB_FLAG="TAB"):
		self.checkStopFlag ()

		py.PAUSE = self.FAST_PAUSE

		value = self.fields [fieldName]
		Utils.printx (f"Llenando TextField '{fieldName}' : '{value}'...")
		if value != None:
			pyperclip_copy (value)
			py.hotkey ("ctrl", "v")
			py.sleep (self.SLOW_PAUSE)

		if TAB_FLAG == "TAB":
			py.press ("Tab")

		py.PAUSE = self.NORMAL_PAUSE

	#---------------------------------------------------------
	# Check if GUI has stopped the bot typing
	#---------------------------------------------------------
	def checkStopFlag (self):
		stopFlagFilename = "flag-bot-stop.flag"
		if os.path.exists (stopFlagFilename):
			raise EcudocBotStopException ()

	#--------------------------------------------------------------------
	#-- Fill combo box pasting text and selecting first value.
	#-- Without check. Default value, if not found. 
	#--------------------------------------------------------------------
	def fillBox (self, fieldName, TAB_FLAG="TAB"):
		py.PAUSE = self.FAST_PAUSE

		fieldValue = self.fields [fieldName]
		Utils.printx (f"Llenando CombolBox '{fieldName}' : '{fieldValue}'...")
		if fieldValue == None:
			return

		pyperclip_copy (fieldValue)
		py.hotkey ("ctrl", "v")
		py.sleep (self.SLOW_PAUSE)
		py.press ("down")
		py.sleep (self.SLOW_PAUSE)

		if TAB_FLAG == "TAB":
			py.press ("Tab")

		py.PAUSE = self.NORMAL_PAUSE

	#-- Fill box and wait if wait cursor appears
	def fillBoxNoDown (self, fieldName, TAB_FLAG="TAB_CHECK"):
		return self.fillBoxWait (fieldName, TAB_FLAG="TAB_CHECK|NODOWN")

	#-- For combo box: select option, down, enter, tab
	#-- Return True if option is selected, False otherwise.
	def fillBoxWait (self, fieldName, TAB_FLAG="TAB_CHECK"):
		self.checkStopFlag ()
		try:
			py.PAUSE = self.NORMAL_PAUSE
			fieldValue = self.fields [fieldName]
			Utils.printx (f"Llenando ComboBox '{fieldName}' : '{fieldValue}'...")
			if fieldValue == None:
				py.press ("Enter") if "NOTAB" in TAB_FLAG else py.press ("Tab")
				return False

			pyperclip_copy (fieldValue)
			py.hotkey ("ctrl", "v"); 
			py.sleep (self.NORMAL_PAUSE)
			if not "NODOWN" in TAB_FLAG:
				py.press ("down") 
			py.press ("Enter")
			py.sleep (self.FAST_PAUSE); self.waitForInfo (); py.sleep (self.FAST_PAUSE)
			if "NOTAB" not in TAB_FLAG:
				py.press ("TAB")
			return True
		finally:
			py.PAUSE = self.NORMAL_PAUSE

	#--------------------------------------------------------------------
	# Wait until 'ready' cursor is present
	#--------------------------------------------------------------------
	def waitForInfo (self, confineMouse=True):
		import win32gui as w32     
		waitCursorId  = 244122955
		readyCursorId = 65539

		self.mouseController.release_mouse ()
		py.sleep (0.1)
		while True:
			self.checkStopFlag ()
			info = w32.GetCursorInfo ()
			id	 = info [1]
			if id > 100000:
				print ("+++ Esperando datos desde el ECUAPASS...")
				py.sleep (self.NORMAL_PAUSE)
			else:
				break
		py.sleep (self.NORMAL_PAUSE)
		if confineMouse:
			self.mouseController.confine_mouse ()

	#--------------------------------------------------------------------
	# Select value in combo box by pasting, checking, and pasting
	# Return true if selected, raise an exception in other case.
	#--------------------------------------------------------------------
	def fillBoxCheck (self, fieldName, TAB_FLAG="TAB_CHECK"):
		try:
			fieldValue = self.fields [fieldName]
			Utils.printx (f"Llenando ComboBox '{fieldName}' : '{fieldValue}'...")
			if fieldValue == None:
				py.press ("Enter") if "NOTAB" in TAB_FLAG else py.press ("Tab")
				return True

			py.PAUSE = self.NORMAL_PAUSE
			for i in range (10):
				self.checkStopFlag ()
				pyperclip_copy (fieldValue)
				py.hotkey ("ctrl", "v"); py.sleep (0.05);py.press ("down"); 
				pyperclip_copy ("")

				py.hotkey ("ctrl","c"); 
				text = pyperclip_paste().lower()
				Utils.printx (f"...Intento {i}: Buscando '{fieldValue}' en texto '{text}'")

				if fieldValue.lower() in text.lower():
					py.PAUSE = 0.3
					pyperclip_copy (fieldValue)
					py.hotkey ("ctrl", "v"); py.press ("enter"); py.sleep (0.01)
					#py.hotkey ("ctrl", "v"); 
					py.PAUSE = self.NORMAL_PAUSE

					#py.press ("TAB") if TAB_FLAG == "TAB" else py.press ("Enter")
					py.press ("Enter") if "NOTAB" in TAB_FLAG else py.press ("Tab")

					Utils.printx (f"...Encontrado '{fieldValue}' en '{text}'")
					return True
				else:
					py.PAUSE += 0.01

				py.hotkey ("ctrl", "a"); py.press ("backspace");

			# Check or not check
			if "NOCHECK" in TAB_FLAG:
				return True
			else:
				message = f"BOTERROR::Problemas en el ECUAPASS sincronizando '{fieldName}':'{fieldValue}'"
				raise Exception (message)
		finally:
			py.PAUSE = self.NORMAL_PAUSE


	#--------------------------------------------------------------------
	# Skip N cells forward or backward 
	#--------------------------------------------------------------------
	def skipN (self, N, direction="RIGHT"):
		py.PAUSE = self.FAST_PAUSE

		if direction == "RIGHT":
			[py.press ("Tab") for i in range (N)]
		elif direction == "LEFT":
			[py.hotkey ("shift", "Tab") for i in range (N)]
		else:
			print (f"Direccion '{direction}' desconocida ")

		py.PAUSE = self.NORMAL_PAUSE
		py.sleep (0.1)

	#------------------------------------------------------------------
	#-- Fill box iterating, copying, comparing.
	#------------------------------------------------------------------
	def fillBoxIter (self, fieldValue, TAB_FLAG="TAB"):
		py.PAUSE = self.NORMAL_PAUSE
		fieldValue = fieldValue.upper ()
		Utils.printx (f"Buscando '{fieldValue}'...")

		for i in range (10):
			lastText = ""
			py.press ("home")
			while True:
				self.checkStopFlag ()
				py.press ("down"); py.sleep (0.1)
				py.hotkey ("ctrl", "a", "c"); py.sleep (0.1)
				text = pyperclip_paste().upper()
				if fieldValue in text:
					Utils.printx (f"...Intento {i}: Encontrado {fieldValue} en {text}") 
					[py.press ("Tab") if TAB_FLAG=="TAB" else py.press ("enter")] 
					return

				if (text == lastText):
					Utils.printx (f"...Intento {i}: Buscando '{fieldValue}' en {text}")
					break
				lastText = text 
			py.sleep (0.2)

		Utils.printx (f"...No se pudo encontrar '{fieldValue}'")
		py.PAUSE = self.NORMAL_PAUSE
		if TAB_FLAG == "TAB":
			py.press ("Tab")

	#-------------------------------------------------------------------
	#-- Fill Date box widget (month, year, day)
	#-------------------------------------------------------------------
	def fillDate (self, fieldName, GET=True):
		text = self.fields [fieldName]
		py.PAUSE = self.NORMAL_PAUSE
		try:
			Utils.printx (f"Llenando campo Fecha '{fieldName}' : {self.fields [fieldName]}'...")
			if (text == None):
				return

			items = text.split("-")
			day, month, year = int (items[0]), int (items[1]), int (items[2])

			currentDate = datetime.datetime.now ()
			if GET:
				currentDate  = self.getBoxDate ()

			dayBox		= currentDate.day
			monthBox	= currentDate.month
			yearBox		= currentDate.year
			Utils.printx (f"...Fecha actual: {dayBox}-{monthBox}-{yearBox}.")

			py.hotkey ("ctrl", "down")
			#py.PAUSE = self.FAST_PAUSE
			self.setYear  (year, yearBox)
			self.setMonth (month, monthBox)
			self.setDay (day)
			#py.PAUSE = self.NORMAL_PAUSE
		except EcudocBotStopException as ex:
			raise EcudocBotStopException ("BOTERROR::Digitación interrumpida")
		except Exception as ex:
			raise EcudocTypingError (f"BOTERROR::Error digitando fecha desde texto '{text}':\n" + str (ex)) 

	#-- Set year
	def setYear (self, yearDoc, yearOCR):
		diff = yearDoc - yearOCR
		pageKey = "pageup" if diff < 0 else "pagedown"
		pageSign = "-" if diff < 0 else "+"

		for i in range (abs(diff)):
			py.hotkey ("shift", pageSign)

	#-- Set month
	def setMonth (self, monthDoc, monthOCR):											 
		diff = monthDoc - monthOCR
		pageKey = "pageup" if diff < 0 else "pagedown"

		for i in range (abs(diff)):
			py.press (pageKey)

	#-- Set day
	def setDay (self, dayDoc):
			nWeeks = dayDoc // 7
			nDays  = dayDoc % 7 - 1

			py.press ("home")
			[py.press ("down") for i in range (nWeeks)]
			if nDays > 0:
				[py.press ("right") for i in range (nDays)]
			elif nDays < 0:
				[py.press ("left") for i in range (abs (nDays))]

			py.press ("enter")

	#-- Get current date from date box widget
	def getBoxDate (self):
		count = 0
		while True:
			self.checkStopFlag ()
			count += 1
			py.hotkey ("ctrl", "down")
			py.press ("home")
			py.hotkey ("ctrl", "a")
			py.hotkey ("ctrl", "c")
			text	 = pyperclip_paste ()

			reFecha = r'\d{1,2}/\d{1,2}/\d{4}'
			if re.match (reFecha, text):
				boxDate  = text.split ("/") 
				boxDate  = [int (x) for x in boxDate]
				class BoxDate:
					day = boxDate[0]; month = boxDate [1]; year = boxDate [2]
				return (BoxDate())

			if (count > 112):
				raise EcudocTypingError ("BOTERROR::Error buscando dias en fecha.")

	#----------------------------------------------------------------
	#-- Function for windows management
	#----------------------------------------------------------------
	def activateWindowByTitle (self, titleString):
		SLEEP=0.2
		ecuWin = self.detectWindowByTitle (titleString)
		Utils.printx (f"Activando ventana '{titleString}'...", ecuWin)
		
		#ecuWin.activate (); py.sleep (SLEEP)
		if ecuWin.isMinimized:
			ecuWin.activate (); py.sleep (SLEEP)

		return (ecuWin)

	#-- Detect ECUAPASS window
	def detectWindowByTitle (self, titleString):
		Utils.printx (f"Detectando ventana '{titleString}'...")
		windows = py.getAllWindows ()
		for win in windows:
			if titleString in win.title:
				return win

		raise EcudocEcuapassException (f"BOTERROR::No se detectó ventana '{titleString}' ")

	#-- For EcuapassDocs window
	def activateEcuapassDocsWindow (self):
		return self.activateWindowByTitle ('Ecuapass-Docs')


	#-- Maximize window by minimizing and maximizing
	def maximizeWindow (self, win):
		SLEEP=0.3
		py.PAUSE = self.SLOW_PAUSE
		win.minimize (); py.sleep (SLEEP)
		win.restore (); py.sleep (0.1)
		py.hotkey ("win", "up")
		py.PAUSE = self.NORMAL_PAUSE
		#win.activate (); #py.sleep (SLEEP)
		#win.resizeTo (py.size()[0].size()[1]); py.sleep (SLEEP)

	def maximizeWindowByClickOnIcon (self, win):
		imagePath = Utils.getPathImage ("image-icon-maximize.png")
		xy = py.locateCenterOnScreen (imagePath, confidence=0.70, grayscale=False)
		if (xy):
			Utils.printx ("+++ DEBUG:Maximizando ventana...")
			py.click (xy[0], xy[1], interval=1)    
			return True
		return False

	#-- Move mouse to center of ecuapass window
	def moveMouseToEcuapassWinCenter (self):
		import win32gui as w32     
		hwnd = w32.FindWindow(None, self.ecuapassWinTitle)

		if hwnd == 0:
			print(f"No se encontrO ventana con tItulo'{self.ecuapassWinTitle}'!")
			return False

		winRect = w32.GetWindowRect(hwnd)
		x0, x1, y0, y1 = winRect[0], winRect [2], winRect [1], winRect [3]
		xc = x0 + (x1 - x0) / 2
		yc = y0 + (y1 - y0) / 2

		x, y = w32.GetCursorPos()
		py.moveTo (xc, yc)

	#-- Locate on MenuIzquierdo button. 
	def locateOnMenuIzquierdo (self, CLICK=True): # Raises ImageNotFoundException
		try:
			Utils.printx ("Localizando botón Menu Izquierdo...")
			xy = EcuBot.findEcuapassImage ("image-button-MenuIzquierdo", CONFIDENCE=0.70)
			Utils.printx (f"...Localizando botón MenuIzquierdo en x: {xy[0]} y: {xy[1]}")
			if CLICK:
				self.mouseController.release_mouse ()
				py.click (xy[0], xy[1], interval=1)    
				py.sleep (0.2)
				self.mouseController.confine_mouse ()
				self.skipN (14)
			return True
		except Exception as ex:
			raise EcuerrorImageNotFound ("BOTERROR::No Localizado botón MenuIzquierdo") from ex

	#-- Locate on Abrir/Cerrar button
	def locateOnAbrirCerrar (self):
		try:
			Utils.printx ("Localizando botón de Abrir-Cerrar...")
			xy = EcuBot.findEcuapassImage ("image-button-AbrirCerrar")
			Utils.printx (f"...Localizando botón de Abrir-Cerrar en x: {xy[0]} y: {xy[1]}")
			py.click (xy[0], xy[1], interval=1)    
			py.click (xy[0], xy[1], interval=1)    
		except ImageNotFoundException as ex:
			Utils.printx ("No se detectó botón de borrado")

	#-- Clear previous webpage content clicking on "ClearPage" button
	def locateOnCleanPage (self):
		try:
			Utils.printx ("Localizando botón de borrado...")
			xy = EcuBot.findEcuapassImage ("image-button-ClearPage")
			py.click (xy[0], xy[1], interval=1)    
			return True
		except ImageNotFoundException as ex:
			Utils.printx ("No se detectó botón de borrado")

	def scrollWindowToBeginning ():
		py.hotkey ("ctrl", "+"); py.press ("backspace");

	#-- Scroll to the page beginning 
#	def scrollWindowToBeginning (self):
#		try:
#			Utils.printx ("Desplazando página hasta el inicio...")
#			xy = EcuBot.findEcuapassImage ("image-button-ScrollUp")
#			py.mouseDown (xy[0], xy[1])
#			py.sleep (2)
#			py.mouseUp (xy[0], xy[1])
#	
#		except ImageNotFoundException as ex:
#			Utils.printx ("No se pudo desplazar la página ECUAPASS al inicio")
	
	#-- Scroll down/up N times (30 pixels each scroll)
	def scrollN (self, N, direction="down"):
		py.PAUSE = self.NORMAL_PAUSE
		sizeScroll = -10000 if direction=="down" else 10000

		for i in range (N):
			self.mouseController.physical_scroll (sizeScroll)                       # Default pyautogui scroll

	#-- Check if active webpage contains correct text 
	def detectEcuapassDocumentPage (self, docType):
		Utils.printx (f"Detectando página de '{docType}' activa...")
		docFilename = "";
		if docType == "CARTAPORTE":
			docFilename = "image-text-Cartaporte"; 
		elif docType == "MANIFIESTO":
			docFilename = "image-text-Manifiesto"; 
		elif docType == "DECLARACION":
			docFilename = "image-text-DeclaracionTransito.png"; 

		filePaths = Utils.getPathImage (docFilename)
		for fpath in filePaths:
			Utils.printx (">>> Probando: ", os.path.basename (fpath))
			xy = py.locateCenterOnScreen (fpath, confidence=0.80, grayscale=True)
			if (xy):
				Utils.printx (">>> Detectado")
				return True

		raise EcudocEcuapassException (f"BOTERROR::No se detectó la página de '{docType}'")

#--------------------------------------------------------------------
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()
	
