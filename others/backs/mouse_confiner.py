import win32gui
import win32con
import pyautogui
import time
from ctypes import wintypes, byref, windll
import ctypes

# For confiner
import pyautogui as py

class MouseConfiner:
	def __init__(self, left, top, right, bottom):
		"""Initialize with screen coordinates of confinement area"""
		self.confined_rect = (left, top, right, bottom)
		self.original_clip = wintypes.RECT()
		windll.user32.GetClipCursor(byref(self.original_clip))

	def __enter__(self):
		"""Activate confinement"""
		clip_rect = wintypes.RECT(*self.confined_rect)
		windll.user32.ClipCursor(byref(clip_rect))
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		"""Release confinement"""
		windll.user32.ClipCursor(byref(self.original_clip))

	def temporary_release(self, duration=0.5):
		"""Temporarily release confinement for scrolling"""
		print (f"+++ Temporarily release confinement for scrolling...")
		windll.user32.ClipCursor(None)
		time.sleep(duration)  # Allow time for scroll operation

		# Call this after ClipCursor(None)
		send_physical_mouse_nudge()
		# Re-confine mouse
		#clip_rect = wintypes.RECT(*self.confined_rect)
		#windll.user32.ClipCursor(byref(clip_rect))

	
	#-------------------------------------------------------------------
	# Other Confine/Release mouse to a user defined area
	#-------------------------------------------------------------------
	def confine_mouse ():
		x1, y1, x2, y2 = Globals.x, Globals.y, Globals.width, Globals.height
		rect = ctypes.wintypes.RECT (x1, y1, x2, y2)
		ctypes.windll.user32.ClipCursor(ctypes.byref(rect))

	def release_mouse():
		ctypes.windll.user32.ClipCursor (None)		
		x, y = py.position()
		py.moveTo (x+1, y+1)
		py.moveTo (x, y)
		py.sleep (0.05)  # tiny wait after the movement

	def scroll_legacy_window (scroll_amount):
		import win32gui
		import ctypes
		import struct
		"""
		Scroll a legacy window using direct messages with proper negative value handling
		:param window_title: Title of target window
		:param scroll_amount: Same values as pyautogui.scroll() (negative = down)
		"""
		WHEEL_DELTA = 120
		WM_MOUSEWHEEL = 0x020A
		
		window_title = 'ECUAPASS - SENAE browser'
		hwnd = win32gui.FindWindow(None, window_title)
		if not hwnd:
			raise Exception(f"Window '{window_title}' not found")
		
		# Convert pyautogui-style scroll amount to WM_MOUSEWHEEL format
		wheel_units = int((scroll_amount / WHEEL_DELTA) * 65536)
		
		# Handle negative values correctly using two's complement
		if wheel_units < 0:
			wheel_units = (1 << 32) + wheel_units  # Convert to unsigned equivalent
		
		# Pack as unsigned long
		wParam = struct.pack('<L', wheel_units)
		
		# Send the scroll message
		ctypes.windll.user32.SendMessageW(
			hwnd,
			WM_MOUSEWHEEL,
			int.from_bytes(wParam, 'little'),  # Properly formatted wParam
			0  # lParam (position)
		)


#--------------------------------------------------------------------
#--------------------------------------------------------------------
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT)]

def send_physical_mouse_nudge():
	print (f"+++ Sending physical movement...")
	mi = MOUSEINPUT(1, 0, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(ctypes.c_ulong(0)))
	inp = INPUT(INPUT_MOUSE, mi)
	windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

def fill_form_with_scroll(confiner):
    """Form filling that includes scrolling"""
    pyautogui.PAUSE = 0.3  # Slower execution for reliability
    
    # Example form filling (replace with your coordinates)
    pyautogui.click(500, 300)  # First field
    pyautogui.typewrite("John Doe")
    
    # When needing to scroll:
    confiner.temporary_release(0.7)  # Release for longer scroll
    pyautogui.scroll(-10000)  # Your large scroll amount
    time.sleep(0.3)  # Wait for scroll to complete
    
    # Continue with form filling (mouse automatically re-confined)
    pyautogui.click(500, 400)
    pyautogui.typewrite("123 Main St")

if __name__ == "__main__":
    # Define your Java modal dialog coordinates (left, top, right, bottom)
    modal_coords = (100, 100, 400, 300)  # Replace with your actual coordinates
    
    with MouseConfiner(*modal_coords) as confiner:
        print("Mouse confined to modal dialog area. Starting form filling...")
        fill_form_with_scroll(confiner)
        print("Form filling complete!")
    
    print("Mouse confinement released.")

