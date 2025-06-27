#!/usr/bin/env python3

import re

def extract_company_info(text):
    """
    Extracts company information from a string with:
    1. Company name (one or more words at start)
    2. Document type and number (NIT/RUC with number)
    3. Company address (one or more words)
    4. City and country (with various separators)
    """
    # First find the document info which is our anchor point
    doc_match = re.search(r'(NIT|RUC)\s*[:#.]*\s*([\d.\-]+)', text, re.IGNORECASE)
    if not doc_match:
        return None
    
    doc_type = doc_match.group(1).upper()
    doc_number = doc_match.group(2)
    doc_start, doc_end = doc_match.span()
    
    # Extract company name (everything before the document info)
    company_name = text[:doc_start].strip()
    
    # The remaining text after document info
    remaining_text = text[doc_end:].strip()
    
    # Improved pattern to handle complex cases
    # Look for country first, then city before it, rest is address
    country_pattern = r'''
        (?:.*\s)?                # Optional preceding text
        ([A-Za-zÁ-Úá-ú]+)        # City (word characters with accents)
        \s*                      # Optional whitespace
        (?:[, -]\s*)?            # Optional separator
        (COLOMBIA|ECUADOR|PERU)  # Country
        \s*$                     # End of string
    '''
    country_match = re.search(country_pattern, remaining_text, re.IGNORECASE | re.VERBOSE)
    
    if not country_match:
        return None
    
    city = country_match.group(1).strip()
    country = country_match.group(2).upper()
    
    # Find everything before the city/country match
    city_start = country_match.start(1)
    address = remaining_text[:city_start].strip()
    
    return {
        'company_name': company_name,
        'document_type': doc_type,
        'document_number': doc_number,
        'address': address,
        'city': city,
        'country': country
    }

# Test cases including the problematic case
test_strings = [
	"ADITIVOS Y QUIMICOS S.A. NIT: 811.002.480-3 VIA SAN JOSE KM 1.5 MED-BTA -\
	GUARNE, ANTIOQUIA - COLOMBIA",
	"ECUADPREMEX S.A. RUC: 1791968891001 AV. PAMPITE N.133 ED YOO P 6 OF 605,\
	QUITO - ECUADOR",
	"PREMEX S.A.S. NIT. 890.922.549-7 CARRERA 50 No 2 SUR 251, AUT SUR,\
	MEDELLIN, ANTIOQUIA - COLOMBIA",
	"ECUADPREMEX S.A. RUC: 1791968891001 AV. PAMPITE N.133 ED YOO P 6 OF 605,\
	QUITO - ECUADOR",
	"LANSEY S.A. RUC 0991248021001 AV AMERICA N39.285 Y CALLE VOZ ANDES\
	SECTOR AV AMERICA LA Y QUITO ECUADOR",
	"TENARIS TUBOCARIBE LTDA NIT: 800011987-3 PARQUE IND C VELEZ POMBO KM\
	1 VIA TURBACO, CARTAGENA COLOMBIA",
	"TENARIS GLOBAL SERVICES ECUADOR S.A. RUC # 1791901460001 LIZARDO\
	GARCIA E10-80 QUITO ECUADOR"

#    "Grupo Industrial Andino RUC 0991248021001 Av. Javier Prado 1000 LIMA - PERU",
#    "Empresa del Estado S.A. NIT: 800011987-3 Calle 123 #45-67 CARTAGENA COLOMBIA",
#    "Compañía de Telecomunicaciones Ltda. RUC # 1791901460001 Av. Amazonas N10-20 QUITO ECUADOR",
#    "Servicios Integrales del Norte S.A.S. NIT. 890.922.549-7 Carrera 7 #71-52 BOGOTA, COLOMBIA",
#    "Distribuidora de Alimentos S.A. NIT: 811.002.480-3 Diagonal 25 #1-80 MEDELLIN, ANTIOQUIA - COLOMBIA",
#    "Consultoría Profesional & Asociados RUC: 1791968891001 Av. 6 de Diciembre N40-120 QUITO - ECUADOR",
#	'Grupo Industrial Andino RUC 0991248021001 Av. Javier Prado 1000 LIMA - PERU'
]

for test in test_strings:
    result = extract_company_info(test)
    print(f"\nInput: '{test}'")
    print("Extracted:", result)
