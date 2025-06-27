from .scraping_doc import ScrapingDoc

from .scraping_doc_web import ScrapingDocWeb
from .scraping_doc_web_CODEBIN import ScrapingDocWeb_CODEBIN
from .scraping_doc_web_ALDIA import ScrapingDocWeb_ALDIA

from .scraping_doc_pdf import ScrapingDocPdf
from .scraping_doc_pdf_static import ScrapingDocPdf_Static
from .scraping_doc_pdf_dynamic import ScrapingDocPdf_Dynamic
from .scraping_doc_pdf_dynamic_TRANSCOMERINTER import ScrapingDocPdfDynamic_TRANSCOMERINTER
from .scraping_doc_pdf_dynamic_SANCHEZPOLO import ScrapingDocPdfDynamic_SANCHEZPOLO
from .scraping_doc_pdf_BOTEROSOTO import ScrapingDocPdf_BOTEROSOTO

from .scraping_doc_pdf_ALDIA import ScrapingDocPdf_ALDIA

__all__ = ["ScrapingDoc", 
           "ScrapingDocWeb", "ScrapingDocWeb_CODEBIN", "ScrapingDocWeb_ALDIA",
		   "ScrapingDocPdf", "ScrapingDocPdf_Static", "ScrapingDocPdf_Dynamic",
		   "ScrapingDocPdfDynamic_TRANSCOMERINTER", "ScrapingDocPdfDynamic_SANCHEZPOLO",
		   "ScrapingDocPdf_ALDIA", "ScrapingDocPdf_BOTEROSOTO"
		   ]
