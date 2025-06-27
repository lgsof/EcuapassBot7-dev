package pdfdocs;

/*
 * Base class for PDF documents 'empresa'
 */
import documento.DocModel;
import exceptions.EcuapassExceptions;
import exceptions.EcuapassExceptions.PdfDocError;
import java.awt.Rectangle;
import java.awt.geom.Rectangle2D;
import java.io.File;
import java.io.IOException;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import main.Utils;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.text.PDFTextStripperByArea;

public abstract class PdfDocument {

    String empresa;
    String tokenEmpresa;     // String to validate empresa
    Rectangle coordsEmpresaCPI, coordsEmpresaMCI = null;
    Rectangle coordsDocTypeCPI, coordsDocTypeMCI = null;
    Rectangle coordsDocNumberCPI = null, coordsDocNumberMCI = null;
    Rectangle coordsDocPaisCPI_1 = null, coordsDocPaisCPI_2 = null;  // 06_Recepcion or 02_Remitente
    Rectangle coordsDocPaisMCI_1 = null, coordsDocPaisMCI_2 = null; // 23_LugarPaisCarga or 06_PlacaPaisVehiculo

    String pdfFilepath;
    PDDocument document;
    PDPage currentPage;
    String docType;
    String[] paises = DocModel.paises;

    public PdfDocument(String empresa) {
        this.empresa = empresa;
    }

    public void open(String pdfFilepath) throws PdfDocError {
        try {
            this.pdfFilepath = pdfFilepath;
            File file = new File(pdfFilepath);
            // Silence PDFBox warnings
            Logger pdfboxLogger = Logger.getLogger("org.apache.pdfbox");
            pdfboxLogger.setLevel(java.util.logging.Level.SEVERE);

            document = PDDocument.load(file);
            currentPage = document.getPage(0); 	// Get the first page of the PDF
        } catch (IOException ex) {
            throw new PdfDocError("No se pudo abrir archivo PDF: " + pdfFilepath);
        }
    }

    public void close() throws PdfDocError {
        try {
            document.close();
        } catch (IOException ex) {
            throw new PdfDocError("No se pudo cerrar archivo PDF: " + pdfFilepath);
        }
    }

    public String extractDocType(String dummyFilename) {
        return Utils.getDocumentTypeFromFilename(dummyFilename);
    }

    public String extractDocType() throws PdfDocError {
        String text = this.extractTextFromRegion(this.coordsDocTypeCPI);

        if (text.toUpperCase().contains("CARTA DE PORTE") || text.toUpperCase().contains("CPIC")) {
            this.docType = "CARTAPORTE";
        } else {
            text = this.extractTextFromRegion(this.coordsDocTypeMCI);
            if (text.toUpperCase().contains("MANIFIESTO") || text.toUpperCase().contains("MCI")) {
                this.docType = "MANIFIESTO";
            } else {
                throw new PdfDocError("ERROR: Determinando el tipo de documento desde el PDF: " + new File(this.pdfFilepath).getName());
            }
        }
        return this.docType;
    }

    public String getCheckEmpresaFromToken() throws PdfDocError, EcuapassExceptions.AppDocAccessError {
        Rectangle[] coords = {coordsEmpresaCPI, coordsEmpresaMCI};
        for (Rectangle coord : coords) {
            String text = this.extractTextFromRegion(coord);
            if (text.contains (tokenEmpresa)) {
                return this.empresa;
            }
        }
        throw new EcuapassExceptions.AppDocAccessError("ERROR: Problemas validando el Token de la Empresa desde el PDF");
    }

    public String extractNumber(String dummyFilename) {
        return Utils.extractDocNumber(dummyFilename);
    }

    public String extractNumber() throws PdfDocError {
        String docNumber = null;
        if (this.extractDocType().equals("CARTAPORTE")) {
            docNumber = this.extractTextFromRegion(coordsDocNumberCPI);
        } else if (this.extractDocType().equals("MANIFIESTO")) {
            docNumber = this.extractTextFromRegion(coordsDocNumberMCI);
        } else {
            throw new PdfDocError("ERROR::Tipo de documento desconocido.");
        }

        String reDocNumber = "(?:No\\.\\s*)?([\\S]+)$";
        Pattern pattern = Pattern.compile(reDocNumber);
        Matcher matcher = pattern.matcher(docNumber);
        if (matcher.find()) {
            return matcher.group(1);
        }
        throw new PdfDocError("ERROR::Extrayendo número de documento desde: " + docNumber);
    }

    public abstract String extractPais(String dummyFilename) throws PdfDocError;

    public String extractPais() throws EcuapassExceptions.PdfDocError {
        Rectangle[] coordsPaisesCPI = new Rectangle[]{coordsDocPaisCPI_1, coordsDocPaisCPI_2};
        Rectangle[] coordsPaisesMCI = new Rectangle[]{coordsDocPaisMCI_1, coordsDocPaisMCI_2};
        Rectangle[] coordsPaises = null;
        if (this.docType.equals("CARTAPORTE")) {
            coordsPaises = coordsPaisesCPI;
        } else if (this.docType.equals("MANIFIESTO")) {
            coordsPaises = coordsPaisesMCI;
        }

        for (Rectangle coords : coordsPaises) {
            String textPais = this.extractTextFromRegion(coords); //06_Recepcion
            String docPais = Utils.extractLastCountry(textPais, paises);
            if (docPais != null && !docPais.isEmpty()) {
                return docPais;
            }
        }
        throw new EcuapassExceptions.PdfDocError("No se pudo identificar país de origen de la carga");
    }

    public String extractTextFromRegion(Rectangle coords) throws PdfDocError {
        int x = coords.x, y = coords.y, width = coords.width, height = coords.height;
        try {
            // Create a Rectangle2D object (which is what PDFTextStripperByArea expects)
            Rectangle2D.Float rect = new Rectangle2D.Float(x, y, width, height);

            // Create a PDFTextStripperByArea to extract text from the defined area
            PDFTextStripperByArea stripper = new PDFTextStripperByArea();
            stripper.addRegion("region1", rect); // Add the defined region
            stripper.extractRegions(currentPage); // Extract the text from the region

            String text = stripper.getTextForRegion("region1");
            return (text);
        } catch (IOException ex) {
            throw new PdfDocError("ERROR: Extrayendo texto desde región");
        }
    }
}
