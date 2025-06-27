import win32api
import pyautogui
import time
from ctypes import wintypes, byref, windll, c_ulong, Structure, POINTER, sizeof

# Enhanced mouse control structure
class MOUSEINPUT(Structure):
	_fields_ = [("dx", c_ulong),
				("dy", c_ulong),
				("mouseData", c_ulong),
				("dwFlags", c_ulong),
				("time", c_ulong),
				("dwExtraInfo", POINTER(c_ulong))]

class Input(Structure):
	_fields_ = [("type", c_ulong),
				("mi", MOUSEINPUT)]

class MouseController:
	def __init__(self, coordinatesString):
		"""Initialize with confinement area coordinates"""
		coords = coordinatesString.split (',')
		self.x1, self.y1, self.x2, self.y2 = int (coords [0]), int (coords [1]), int (coords [2]), int (coords [3])
		self.input_struct = Input()
		self.input_struct.type = 0	# INPUT_MOUSE

	def confine_mouse (self):
		rect = wintypes.RECT (self.x1, self.y1, self.x2, self.y2)
		windll.user32.ClipCursor (byref(rect))

	def release_mouse (self):
		MouseController.RELEASE_MOUSE ()

	def RELEASE_MOUSE ():
		# Temporarily move mouse to center of confined area
		windll.user32.ClipCursor (None)		
		#center_x = self.confined_rect[0] + (self.confined_rect[2] - self.confined_rect[0]) // 2
		#center_y = self.confined_rect[1] + (self.confined_rect[3] - self.confined_rect[1]) // 2
		win32api.SetCursorPos ((100, 300))

	#-- Perform physical scrolling that works with legacy apps. Release...Confiner mouse
	def physical_scroll(self, scroll_amount):
		try:
			self.release_mouse ()
			
			# Generate physical scroll event
			self.input_struct.mi = MOUSEINPUT(0, 0, scroll_amount, 0x0800, 0, None)  # 0x0800 = MOUSEEVENTF_WHEEL
			windll.user32.SendInput(1, byref(self.input_struct), sizeof(self.input_struct))
			time.sleep(0.05)

			self.confine_mouse ()
		except:
			windll.user32.ClipCursor (None)		

