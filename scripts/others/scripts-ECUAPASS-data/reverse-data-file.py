#!/usr/bin/env python3

import sys
args = sys.argv

filename = args [1]

itemList = open (filename).readlines()

n = len (itemList)
print ("N:", n)

for i in range (n, 0, -1):
	print (itemList [i-1], end="")
