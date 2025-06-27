package pdfdocs;

/*
 * Functions for PDF documents of ALDIA 'empresa'
 */
import exceptions.EcuapassExceptions;
import java.awt.Rectangle;
import main.Utils;

public class PdfDocument_ALDIA extends PdfDocument {

	public PdfDocument_ALDIA (String empresa) {
		super (empresa);
		tokenEmpresa = "TRANSERCARGA|SERCARGA";

		coordsEmpresaCPI = new Rectangle (40, 92, 103, 13);
		coordsEmpresaMCI = new Rectangle (30, 116, 96, 13);
		coordsDocTypeCPI = new Rectangle (215, 29, 292, 21);
		coordsDocTypeMCI = new Rectangle (248, 14, 262, 20);
		coordsDocNumberCPI = new Rectangle (431, 59, 110, 17);
		coordsDocNumberMCI = new Rectangle (198, 47, 391, 19);
		
		// Pais coords
		coordsDocPaisCPI_1 = new Rectangle (21, 156, 281, 46); //06_Recepcion
		coordsDocPaisCPI_2 = new Rectangle (304, 122, 286, 18); //02_Remitente
		coordsDocPaisMCI_1 = new Rectangle (23, 349, 279, 13); //23_LugarPaisCarga
		coordsDocPaisMCI_2 = new Rectangle (308, 177, 143, 13); //06_PlacaPaisVehiculo
	}

	@Override
	public String getCheckEmpresaFromToken () throws EcuapassExceptions.AppDocAccessError, EcuapassExceptions.PdfDocError {
		try {
			try {
				this.tokenEmpresa = "TRANSERCARGA";
				if (super.getCheckEmpresaFromToken () != null)
					return "ALDIA::TRANSERCARGA";
			} catch (EcuapassExceptions.PdfDocError ex) {
			}
			this.tokenEmpresa = "SERCARGA";
			if (super.getCheckEmpresaFromToken () != null)
				return "ALDIA::SERCARGA";
			throw new EcuapassExceptions.PdfDocError ("Empresa no reconocida");
		} catch (EcuapassExceptions.PdfDocError ex) {
			throw new EcuapassExceptions.PdfDocError ("Empresa no reconocida");
		}
	}

	public String extractPais (String dummyFilename) {
		return null;
	}
	
}







