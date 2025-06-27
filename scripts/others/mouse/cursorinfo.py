
import win32gui as w32
import pyautogui as py
import time

#--  Checks if the cursor is within the window based on screen position.
def moveCursorToWindowsCenter (window_title):
	hwnd = w32.FindWindow(None, window_title)

	if hwnd == 0:
		print(f"Window with title '{window_title}' not found!")
		return False

	winRect = w32.GetWindowRect(hwnd)
	x0, x1, y0, y1 = winRect[0], winRect [2], winRect [1], winRect [3]
	xc = x0 + (x1 - x0) / 2
	yc = y0 + (y1 - y0) / 2

	x, y = w32.GetCursorPos()
	print ("Cur pos:", x,y)
	print ("Win center:", xc,yc)
	time.sleep (3)
	py.moveTo (xc, yc)
	py.click ()
	x, y = w32.GetCursorPos()
	print ("Cur pos:", x,y)

	#cursor_x, cursor_y = win32gui.GetCursorPos()

	#return (
	#	cursor_x >= winRect[0] and
	#	cursor_x <= winRect[2] and
	#	cursor_y >= winRect[1] and
	#	cursor_y <= winRect[3]
	#)



winTitle = "ECUAPASS - SENAE browser"
moveCursorToWindowsCenter (winTitle)

oldId = 0
count = 1
while True:
	info = w32.GetCursorInfo ()
	id	 = info [1]
	if id !=oldId:
		print (f">>> # {count}. Id: {id}")
		count += 1
		oldId = id
	time.sleep (0.01)





