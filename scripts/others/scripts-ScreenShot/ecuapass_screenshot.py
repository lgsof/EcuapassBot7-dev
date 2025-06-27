import pygetwindow as gw
import pyautogui
from PIL import Image
import time
import numpy as np

# Find the browser window by title
window_title = 'ECUAPASS - SENAE browser'
window = None

for w in gw.getWindowsWithTitle(window_title):
	if window_title in w.title:
		window = w
		break

if not window:
	print("Browser window not found!")
	exit()

# Bring the window to the front
window.activate()
time.sleep(1)  # Give time to activate

# Define screenshot parameters
x, y, width, height = window.left, window.top, window.width, window.height
scroll_pixels = height - 100  # Scroll by nearly one full screen height
screenshots = []

# Take screenshots while scrolling
while True:
	screenshot = pyautogui.screenshot(region=(x, y, width, height))
	screenshots.append(screenshot)

	# Scroll down
	pyautogui.scroll(-scroll_pixels)
	time.sleep(1)  # Wait for the page to render

	# Check if we reached the bottom (by comparing last two images)
	if len(screenshots) > 1 and np.array_equal(
		np.array(screenshots[-1]), np.array(screenshots[-2])
	):
		break  # Stop if the last screenshot is identical to the previous one

# Stitch images together
total_height = sum(img.height for img in screenshots)
stitched_image = Image.new("RGB", (width, total_height))

y_offset = 0
for img in screenshots:
	stitched_image.paste(img, (0, y_offset))
	y_offset += img.height

# Save the final stitched screenshot
stitched_image.save("full_page_screenshot.png")
print("Full page screenshot saved as 'full_page_screenshot.png'")

