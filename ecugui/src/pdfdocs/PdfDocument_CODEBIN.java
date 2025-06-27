package pdfdocs;

/*
 * Functions for extracting info from PDF documents in 'empresas" using CODEBIN
 */
import exceptions.EcuapassExceptions.PdfDocError;
import java.awt.Rectangle;

public class PdfDocument_CODEBIN extends PdfDocument {

	public PdfDocument_CODEBIN (String empresa, String token) {
		super (empresa);
		this.tokenEmpresa = token;
		coordsDocTypeCPI = new Rectangle (216, 25, 293, 15);
		coordsDocTypeMCI = new Rectangle (220, 24, 315, 16);
		coordsDocNumberCPI = new Rectangle (470, 46, 121, 21);
		coordsDocNumberMCI = new Rectangle (462, 43, 127, 25);
		coordsDocPaisCPI_1 = new Rectangle (418, 46, 34, 21);
		coordsDocPaisMCI_1 = new Rectangle (413, 43, 34, 24);
		
		coordsEmpresaCPI = new Rectangle (23,77,288,76);
		coordsEmpresaMCI = new Rectangle (24,90,289,91);			
	}

	public String extractPais () throws PdfDocError {
		String textPais = null;
		if (this.docType.equals ("CARTAPORTE"))
			textPais = this.extractTextFromRegion (coordsDocPaisCPI_1); // CO | EC | PE
		else if (this.docType.equals ("MANIFIESTO"))
			textPais = this.extractTextFromRegion (coordsDocPaisMCI_1); // CO | EC | PE	

		return this.extractPais (textPais.trim ());
	}

	public String extractPais (String dummyFilename) throws PdfDocError {
		if (dummyFilename.contains ("CO"))
			return "COLOMBIA";
		else if (dummyFilename.contains ("EC"))
			return "ECUADOR";
		else if (dummyFilename.contains ("PE"))
			return "PERU";
		throw new PdfDocError ("ERROR: Extrayendo pais desde PDF " + docType + ": " + pdfFilepath);
	}	
}
