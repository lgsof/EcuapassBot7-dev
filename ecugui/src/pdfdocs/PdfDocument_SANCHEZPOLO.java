package pdfdocs;

/*
 * Functions for PDF documents of ALDIA 'empresa'
 */
import exceptions.EcuapassExceptions;
import java.awt.Rectangle;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import main.Utils;

public class PdfDocument_SANCHEZPOLO extends PdfDocument {

	public PdfDocument_SANCHEZPOLO (String empresa) {
		super (empresa);
		tokenEmpresa = "NIT. 890103161-1";

		coordsEmpresaCPI = new Rectangle (2, 48, 295, 67);
		coordsDocTypeCPI = new Rectangle (298, 2, 293, 17);
		coordsDocNumberCPI = new Rectangle (298, 21, 200, 17);

		coordsEmpresaMCI = new Rectangle (2, 65, 326, 71);
		coordsDocTypeMCI = new Rectangle (299, 3, 294, 20);
		coordsDocNumberMCI = new Rectangle (292, 24, 200, 18);

		coordsDocPaisCPI_1 = new Rectangle (298, 123, 295, 15); //06_Recepcion
		coordsDocPaisCPI_2 = new Rectangle (3, 125, 294, 49); //02_Remitente
		coordsDocPaisMCI_1 = new Rectangle (4, 371, 294, 20); //23_LugarPaisCarga
		coordsDocPaisMCI_2 = new Rectangle (299, 159, 146, 21); //06_PlacaPaisVehiculo
	}

	public String extractPais (String dummyFilename) throws EcuapassExceptions.PdfDocError {
		return null;
	}
}
