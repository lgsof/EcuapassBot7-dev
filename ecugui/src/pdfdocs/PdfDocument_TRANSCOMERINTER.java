package pdfdocs;

/*
 * Functions for PDF documents of ALDIA 'empresa'
 */
import exceptions.EcuapassExceptions;
import java.awt.Rectangle;

public class PdfDocument_TRANSCOMERINTER extends PdfDocument {

	public PdfDocument_TRANSCOMERINTER (String empresa) {
		super (empresa);
		tokenEmpresa = "RUC: 1791121104001";

		coordsEmpresaCPI   = new Rectangle (20, 78, 278, 86);
		coordsDocTypeCPI   = new Rectangle (187, 12, 221, 43);
		coordsDocNumberCPI = new Rectangle (408,11,167,47);

		coordsEmpresaMCI   = coordsEmpresaCPI;
		coordsDocTypeMCI   = coordsDocTypeCPI;
		coordsDocNumberMCI = coordsDocNumberCPI;

		coordsDocPaisCPI_1 = new Rectangle (299, 127, 275, 37); //06_Recepcion
		coordsDocPaisCPI_2 = new Rectangle (20, 173, 278, 39); //02_Remitente
		coordsDocPaisMCI_1 = new Rectangle (20, 378, 278, 16); //23_LugarPaisCarga
		coordsDocPaisMCI_2 = new Rectangle (297, 177, 140, 26); //06_PlacaPaisVehiculo
	}

	public String extractPais (String dummyFilename) throws EcuapassExceptions.PdfDocError {
		return null;
	}
}
