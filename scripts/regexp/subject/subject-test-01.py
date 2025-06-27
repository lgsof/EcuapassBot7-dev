#!/usr/bin/env python3

import re

def extract_company_info(text):
    """
    Extracts company information from a string with:
    1. Company name (one or more words at start)
    2. Document type and number (NIT/RUC with number)
    3. Company address (one or more words)
    4. City and country (with various separators)
    
    Args:
        text (str): Input string containing company information
        
    Returns:
        dict: Dictionary with extracted information or None if parsing fails
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
    
    # Find the country pattern in the remaining text
    country_match = re.search(
        r'(.+?)\s*(?:[, -]\s*)?(COLOMBIA|ECUADOR|PERU)$', 
        remaining_text, 
        re.IGNORECASE
    )
    if not country_match:
        return None
    
    city_country = country_match.group(0).strip()
    city = country_match.group(1).strip()
    country = country_match.group(2).upper()
    
    # Address is everything between document info and city/country
    address_end_pos = country_match.start()
    address = remaining_text[:address_end_pos].strip()
    
    return {
        'company_name': company_name,
        'document_type': doc_type,
        'document_number': doc_number,
        'address': address,
        'city': city,
        'country': country
    }

# Test cases with multi-word company names
test_strings = [
    "Empresa del Estado S.A. NIT: 800011987-3 Calle 123 #45-67 CARTAGENA COLOMBIA",
    "Compañía de Telecomunicaciones Ltda. RUC # 1791901460001 Av. Amazonas N10-20 QUITO ECUADOR",
    "Servicios Integrales del Norte S.A.S. NIT. 890.922.549-7 Carrera 7 #71-52 BOGOTA, COLOMBIA",
    "Grupo Industrial Andino RUC 0991248021001 Av. Javier Prado 1000 LIMA - PERU",
    "Distribuidora de Alimentos S.A. NIT: 811.002.480-3 Diagonal 25 #1-80 ANTIOQUIA - COLOMBIA",
    "Consultoría Profesional & Asociados RUC: 1791968891001 Av. 6 de Diciembre N40-120 QUITO - ECUADOR",
    "ABC Corporation NIT 890.901.321-5 Main Street 123 TULCAN, ECUADOR"
]

for test in test_strings:
    result = extract_company_info(test)
    print(f"\nInput: '{test}'")
    print("Extracted:", result)

