package settings;

/*
 * Class for handling settings (init, read, save, get, set, others...)
 */
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.reflect.TypeToken;
import commander.AppCommander;
import documento.DocModel;
import exceptions.EcuapassExceptions;
import exceptions.EcuapassExceptions.SettingsError;
import java.io.File;
import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Base64;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import main.Controller;

public class SettingsController extends Controller {

    File settingsFile = new File(DocModel.runningPath + "/settings.bin");
    Map settings;
    SettingsPanel settingsPanel;

    Controller controller;
    AppCommander appCommander;     // Sends and Handle Python commander events

    public SettingsController(main.Controller controller) {
        this.controller = controller;
        // Init Java AppCommander
        appCommander = new AppCommander(this);
    }
    
    // First time initialization. 
    // If settings.bin exists then read it, else, read and update old "txt" or create a new
    public void initSettings(JFrame parent) throws EcuapassExceptions.SettingsError {
        this.settings = null;
        settingsPanel = new SettingsPanel();
        settingsPanel.setController(this);
        if (this.settingsFile.exists()) {
            this.settings = this.readBinSettings();
            settingsPanel.setValues(settings);
        } else {
            //this.settings = new LinkedHashMap<String, LinkedHashMap<String, String>>();
            settingsPanel.showAsDialog(parent);
            System.exit(0);
        }
    }    

    @Override
    public JFrame getMainView() {
        return controller.getMainView();
    }

    @Override
    public void buscarEmpresaCodebini(String codebiniId) {
        appCommander.buscarEmpresaCodebini(codebiniId);
    }

    @Override
    public void onRespuestaEmpresaCodebini(String empresaCodebini, String URL) {
        if (empresaCodebini.isEmpty()) {
            JOptionPane.showMessageDialog(getMainView(), "Empresa NO encontrada!. Revise el nombre.", "Alerta", JOptionPane.WARNING_MESSAGE);
        } else {
            settingsPanel.setEmpresaCodebini(empresaCodebini, URL);
        }
    }


    public void showAsDialog(JFrame parent) {
        settingsPanel.showAsDialog(parent);
    }

    @Override
    public void onInstallKeyFromCloud(String empresa, String password, String installKeyFromCloud) throws SettingsError {
        if (!installKeyFromCloud.equals(password)) {
            JOptionPane.showMessageDialog(settingsPanel, "Clave Errada!", "Verificación de Acceso", JOptionPane.ERROR_MESSAGE);
            return;
        }

        settingsPanel.enableSettings(true);
        if (settings != null) {
            settingsPanel.setValues(this.settings);
        }
        JOptionPane.showMessageDialog(settingsPanel, "Acceso Habilitado!", "Verificación de Acceso", JOptionPane.INFORMATION_MESSAGE);
    }

    // Event from SettingsPanel
    public void onSalirButton() throws EcuapassExceptions.SettingsError {
        settingsPanel.enableSettings(false);

    }

    public void onSaveSettings(Map settings) {
        if (this.checkForValidSettings(settings) == false) {
            return;
        }
        this.settings = settings;
        this.writeBinSettings(settings);
        appCommander.onSaveSettings (this.settingsFile.toString());
//        controller.onSettingsSaved(); // Notify to Commander
        JOptionPane.showMessageDialog(settingsPanel, "Información Guardada!", "Aviso", JOptionPane.INFORMATION_MESSAGE);
    }

    // Update Data/Document configuration
//    public void onUpdateSettings(Map settings) {
//        this.writeBinSettings(settings);
//        if (this.settings != null) {
//            controller.onSettingsSaved(); // Notify to Commander
//        }
//        this.settings = settings;
//    }

    public void onSendFeedback(String feedbackText) {
        controller.onSendFeedback(feedbackText);
    }

// Read a Json from a binary file encoded Base64
    public Map readBinSettings() {
        try {
            byte[] encodedBytes = Files.readAllBytes(this.settingsFile.toPath());
            byte[] decodedBytes = Base64.getDecoder().decode(encodedBytes);
            String jsonString = new String(decodedBytes, StandardCharsets.UTF_8);

            // Use Gson with explicit type
            Type type = new TypeToken<LinkedHashMap<String, LinkedHashMap<String, String>>>() {
            }.getType();
            return new Gson().fromJson(jsonString, type);
        } catch (Exception ex) {
            Logger.getLogger(SettingsController.class
                    .getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }

    // Write JSON object as binary encoded Base64
    public Map writeBinSettings(Map settings) {
        try {
            Gson gson = new GsonBuilder()
                    .serializeNulls()
                    .setPrettyPrinting()
                    .create();
            String jsonString = gson.toJson(settings);

            // Encode the JSON string to Base64 bytes
            byte[] encodedBytes = Base64.getEncoder().encode(jsonString.getBytes(StandardCharsets.UTF_8));

            // Write the encoded bytes to the binary file
            Files.write(this.settingsFile.toPath(), encodedBytes);

            System.out.println(">>> Guardando archivo de configuracion: " + settingsFile);

        } catch (IOException ex) {
            Logger.getLogger(SettingsController.class
                    .getName()).log(Level.SEVERE, null, ex);
        }
        return settings;
    }

    public SettingsPanel getSettingsPanel() {
        return settingsPanel;
    }

    // Get Json from Map
    public JsonObject getJsonFromMap(Map<String, String> mapSettings) {
        JsonObject jsonObject = new JsonObject();
        for (Map.Entry<String, String> entry : mapSettings.entrySet()) {
            jsonObject.addProperty(entry.getKey(), entry.getValue());
        }
        return jsonObject;
    }

    public boolean checkForValidSettings(Map settings) {
        if (this.getSettingsValue (settings, "datos", "nickname").equals("")) {
            JOptionPane.showMessageDialog(null, "Nombre de empresa inválido");
            return false;
        }
        return true;
    }
    
    public String getNickname () {
        return this.getSettingsValue ("datos", "nickname");
    }
    public String getUrlWeb () {
        return this.getSettingsValue ("datos", "urlWeb");
    }

    // Get value from "settings.json" file located in "runningPath"
    public String getSettingsValue(String key1, String key2) {
        return this.getSettingsValue (this.settings, key1, key2);
    }
    public String getSettingsValue(Map settings, String key1, String key2) {
        Map parentMap = (LinkedHashMap<String, String>) settings.get(key1);
        String value = (String) parentMap.get(key2);
        return value;
    }
    public Map getSettingsValue(String key1) {
        return this.getSettingsValue (this.settings, key1);
    }
    public Map getSettingsValue(Map settings, String key1) {
        Map parentMap = (LinkedHashMap) settings.get(key1);
        return parentMap;
    }

    // Create new 'settings.json' file, if it is old	
    public void createInitialSettings(String empresa) {
    }

    public void printSettings(JsonObject settings) {
        if (settings == null || settings.isEmpty()) {
            System.out.println("Empty settings object.");
            return;
        }

        // Use an iterator to loop through key-value pairs
        Set<Map.Entry<String, JsonElement>> entries = settings.entrySet();
        for (Map.Entry<String, JsonElement> entry : entries) {
            String key = entry.getKey();
            JsonElement value = entry.getValue();

            // Ensure value is a string
            if (!value.isJsonPrimitive() || !value.getAsJsonPrimitive().isString()) {
                System.err.println("Warning: Unexpected value type for key: " + key);
                continue;
            }

            String valueString = value.getAsString();
            System.out.printf("%s: %s\n", key, valueString);
        }
    }

    @Override
    public void disableButtons() {
        this.controller.disableButtons();
    }

    // Print to feedback panel in settings panel
    public void println(String s) {
        settingsPanel.println(s);
    }
}
