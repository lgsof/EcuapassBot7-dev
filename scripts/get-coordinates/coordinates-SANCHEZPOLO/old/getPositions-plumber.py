#!/usr/bin/env python3

import sys
import pdfplumber

pdf_path = sys.argv [1]

with pdfplumber.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        # Get characters with positions
        for char in page.chars:
            print(f"Page {page_number}: Char '{char['text']}' at ({char['x0']}, {char['top']})")

