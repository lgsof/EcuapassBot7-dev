package commander;

import documento.DocModel;
import exceptions.EcuapassExceptions;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import main.Controller;
import main.MainController;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import pdfdocs.PdfDocument;
import settings.SettingsController;

public class AppCommander extends Controller {

    Controller controller;

    public AppCommander(Controller controller) {
        this.controller = controller;
    }

    @Override
    public JFrame getMainView() {
        return controller.getMainView();
    }

    public void onSaveSettings (String settingsFile) {
        try {
            String[] params = {"saved_settings", settingsFile, null, null, null};
            PythonWorker worker = new PythonWorker(this, params);
            worker.execute();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(null, ex.getMessage());
            Logger.getLogger(MainController.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    @Override
    public void onRespuestaEmpresaCodebini (String response) {
        String empresaCodebini = response.split ("::",-1)[1];
        String URL = response.split ("::",-1)[2];
        controller.onRespuestaEmpresaCodebini(empresaCodebini, URL);
    }

    public void getInitialPdfInfo(String pdfFilepathStr, SettingsController settingsEmpresa) {
        try {
            String[] params = {"get_initial_pdf_info", pdfFilepathStr, DocModel.empresa, null, null};
            PythonWorker worker = new PythonWorker(this, params);
            worker.execute();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(null, ex.getMessage());
            Logger.getLogger(MainController.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    // Receives initial PDF info from pycommander
    @Override
    public void onInitialPdfInfo(String pdfInfoJsonString) {
        Map<String, String> pdfInfoMap = new HashMap<>();
        try {
            JSONParser parser = new JSONParser();
            JSONObject pdfJson = (JSONObject) parser.parse(pdfInfoJsonString);
            pdfJson = (JSONObject) pdfJson.get("initialPdfInfo");

            pdfInfoMap.put("docEmpresa", (String) pdfJson.get("docEmpresa"));
            pdfInfoMap.put("docType", (String) pdfJson.get("docType"));
            pdfInfoMap.put("docNumber", (String) pdfJson.get("docNumber"));
            pdfInfoMap.put("docPais", (String) pdfJson.get("docPais"));
            controller.setInitialPdfInfo(pdfInfoMap);

        } catch (ParseException ex) {
            JOptionPane.showMessageDialog(null, ex.getMessage());
            Logger.getLogger(MainController.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    @Override
    public void disableButtons() {
        controller.disableButtons();
    }

    @Override
    public void onEndProcessing(String statusMsg, String texto) {
        controller.onEndProcessing(statusMsg, texto);
    }

    @Override
    public void buscarEmpresaCodebini(String codebiniName) {
        String[] params = {"buscar_empresa_codebini", codebiniName, null, null, null};
        PythonWorker worker = new PythonWorker(this, params);
        worker.execute();
    }
}
