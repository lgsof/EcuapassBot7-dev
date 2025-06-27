#!/usr/bin/env python3
import os, sys, re

reDate =r'\b(?P<day>\d{1,2})\s+(?:DE|DEL)\s+(?P<month>ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)(?:\s+(?:DE|DEL))*\s*(?P<year>\d[.]?\d{3})\b'
text = 'CAJICA COLOMBIA 28 DE ENERO DE 2025'

match = re.search (reDate, text, re.I)

print (match.groups())
