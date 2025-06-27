
import win32gui as w32
import pyautogui as py
import pywinauto
import time


def activateEcuapassWindow ():
	try:
		ecuapassWinTitle = 'ECUAPASS - SENAE browser'
		print ("Activando la ventana del ECUAPASS...")

		# Connect to an existing instance of an application by its title
		app = pywinauto.Application().connect (title=ecuapassWinTitle)

		# Get a reference to the main window and activate it
		ecuapass_window = app.window (title=ecuapassWinTitle)
		ecuapass_window.set_focus()
		return ecuapass_window
	except pywinauto.ElementNotFoundError:
		raise Exception (f"No está abierta la ventana del ECUAPASS")

#--  Checks if the cursor is within the window based on screen position.
def moveCursorToWindowsLeft (window_title):
	hwnd = w32.FindWindow(None, window_title)

	if hwnd == 0:
		print(f"Window with title '{window_title}' not found!")
		return False

	winRect = w32.GetWindowRect(hwnd)
	x0, x1, y0, y1 = winRect[0], winRect [2], winRect [1], winRect [3]
	print (f"x0:{x0}, x1:{x1}, y0:{y0}, y1:{y1}")
	xl = x1 - (x1 - x0) / 16
	yl = y0 + 10

	print ("Win left:", xl,yl)
	py.moveTo (xl, yl)
	py.sleep (1)
	py.click ()
	py.sleep (1)

def maximizeWindow ():
	imgName = "image00-icon-maximize.png"
	xy = py.locateCenterOnScreen (imgName, confidence=0.90, grayscale=True)
	print (xy)
	if (xy):
		print ("...Detectado:", imgName)
		py.click (*xy)
		return True

winTitle = "ECUAPASS - SENAE browser"
activateEcuapassWindow ()
moveCursorToWindowsLeft (winTitle)
#maximizeWindow ()

i = 0
while i < 5:
	print ("Scrolling...", i)
	py.press ("up")
	i += 1
		

