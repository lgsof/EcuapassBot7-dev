import win32gui as w32
import time

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





