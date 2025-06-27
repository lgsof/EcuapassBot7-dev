#!/usr/bin/env python3

import fitz  # PyMuPDF
import sys 
pdf_path = sys.argv [1]

doc = fitz.open(pdf_path)
for page_number, page in enumerate(doc, start=1):
	text_blocks = page.get_text("blocks")  # Get text as blocks (line-level)
	for block in text_blocks:
		x0, y0, x1, y1, text, _, _ = block
		# Filter based on block height or width (remove too small or large ones)
		if (x1 - x0) > 5 and (y1 - y0) > 5:  # Adjust thresholds as needed
			print(f"Page {page_number}: Line '{text.strip()}' at ({x0}, {y0}, {x1}, {y1})")
			print ("-----------------------------------------------------")

