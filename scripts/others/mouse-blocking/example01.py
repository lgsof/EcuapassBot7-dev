import ctypes
import pyautogui
import time

try:
    # Block all user input (mouse + keyboard)
    ctypes.windll.user32.BlockInput(True)
    time.sleep(0.5)  # Optional: small delay to ensure block takes effect

    # Simulate typing
    pyautogui.write("Hello, this is automated input.", interval=0.1)

finally:
    # Always unblock input!
    ctypes.windll.user32.BlockInput(False)

