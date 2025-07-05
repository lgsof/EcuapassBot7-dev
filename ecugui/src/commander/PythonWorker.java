package commander;

import exceptions.EcuapassExceptions;
import javax.swing.*;
import java.util.concurrent.ExecutionException;
import java.util.logging.Level;
import java.util.logging.Logger;
import main.Controller;

public class PythonWorker extends SwingWorker<String, Void> {

    private final Controller controller;
    private final String service;
    private final String param1;
    private final String param2;
    private final String param3;
    private final String param4;

    public PythonWorker(Controller controller, String[] params) {
        this.controller = controller;
        this.service = params[0];
        this.param1 = params[1];
        this.param2 = params[2];
        this.param3 = params[3];
        this.param4 = params[4];
    }

    @Override
    protected String doInBackground() throws Exception {
        // Send the command to Python and get the response
        PythonManager pythonManager = PythonManager.getInstance();
        return pythonManager.sendCommandSync(service, param1, param2, param3, param4); // Use a synchronous send method here
    }

    // Retrieve the result and invoke the success callback
    @Override
    protected void done() {
        try {
            String response = get(); // Gets the result from doInBackground()    
            controller.out (response);     
            response = response.split("::", 2)[1];
            if (response.contains ("respuestaEmpresaCodebini")) {
                controller.onRespuestaEmpresaCodebini (response);
            } else if (response.contains("initialPdfInfo")) {
                controller.onInitialPdfInfo(response);
            } else if (response.contains("Nueva actualización")) {
                controller.onNuevaActualizacion ();
            }else if (response.contains("CLOUDINSTKEY")) {
                String cloudPassword = response.split("::")[1];
                String empresa = param1;
                String userPassword = param2;
                controller.onInstallKeyFromCloud(empresa, userPassword, cloudPassword);
            } else if (response.contains("EXITO")) {
                controller.onEndProcessing("EXITO", response);
            } else if (response.contains("Ventana de ECUAPASS activada")) {
                controller.onActivatedEcuapassWindow();
            } else if (response.contains("Documento digitado")) {
                controller.onEndProcessing ("EXITO", response);
            } else if (response.contains("BOTERROR")
                    || response.contains("PDFERROR")
                    || response.contains("CLOUDERROR")
                    || response.contains("SCRAPERROR")
                    || response.contains("WEBERROR")
                    || response.contains("NETERROR")
                    || response.contains("ACCESSERROR")) { // Illegal software installation
                String message = response.split("::")[1];
                controller.onEndProcessing("ERROR", message);
            } 
        } catch (InterruptedException | ExecutionException ex) {
            Logger.getLogger(PythonWorker.class.getName()).log(Level.SEVERE, null, ex);
            JOptionPane.showMessageDialog(null, "Problemas ejecutando Commander", "Alerta Ejecución", JOptionPane.ERROR_MESSAGE);
        } catch (EcuapassExceptions.SettingsError ex) {
            Logger.getLogger(PythonWorker.class.getName()).log(Level.SEVERE, null, ex);            
            JOptionPane.showMessageDialog(null, "Problemas con la configuración de la empresa", "Alerta Configuración", JOptionPane.ERROR_MESSAGE);
        }
    }
}
