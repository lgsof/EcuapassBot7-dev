package main;

import commander.AppCommander;
import settings.FeedbackView;
import documento.DocModel;
import documento.DocRecord;
import pdfdocs.PdfDocument;
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import widgets.ImageViewLens;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JTabbedPane;
import javax.swing.SwingUtilities;
import javax.swing.Timer;
import javax.swing.UIManager;
import org.json.simple.parser.ParseException;
import results.ResultsController;
import widgets.ProgressDialog;
import widgets.TopMessageDialog;
import commander.PythonWorker;
import java.util.Map;
import settings.SettingsController;

public class MainController extends Controller {

    String appRelease = "1.981"; // Resources from root dir. Removed tmp-ecuapassdocs
//	String appRelease = "0.9782"; // Changed split token to |

    DocModel docModel;             // Handles invoice data: selected, processed, and no procesed
    PdfDocument pdfDocument;           // PDF document object with docFields info (CPI or MCI)
    AppCommander appCommander;     // Sends and Handle Python commander events
    MainView mainView;
    InputsView inputsView;
    JTabbedPane tabsPanel;
    ImageViewLens imageView;
    //ResultsView resultsView;
    ResultsController resultsController;

    ProgressDialog progressDialog;     // Dialog showed when document processing starts

    SettingsController settingsController; // Initial configuration parameters
    Timer timer;

    public MainController() {
        try {
            initializeAppData();
            initializeComponents();
            docModel.printGlobalPaths(this);

        } catch (Exception ex) {
            ex.printStackTrace();
            TopMessageDialog.show(null, ex.getMessage());
        }
        appRelease = this.getAppRelease();
        out(">>>>>>>>>>>>>>>> GUI version: " + appRelease + " <<<<<<<<<<<<<<<<<<<<");
    }

    // Initial configuration settings, PdfDocument object, copy resources
    public void initializeAppData() throws Exception {
        // DocModel
        System.setProperty("file.encoding", "UTF-8");
        docModel = new DocModel();
        docModel.initGlobalPaths();

        // Init Java AppCommander
        appCommander = new AppCommander(this);

        // SettingsEmpresa
        settingsController = new SettingsController(this);
        settingsController.initSettings(mainView);
        DocModel.empresa = settingsController.getNickname ();

        // Start python commander with running dir
        String[] params = {"init_application", DocModel.empresa, DocModel.runningPath, null, null};
        PythonWorker worker = new PythonWorker(this, params);
        worker.execute();

        // Resources for cartaporte/manifiesto java forms (e.g. Paises, Distritos,...)
        // OBSOLETE: Resoureces loaded directly from projects root dir
        // docModel.copyResourcesToTempDir();
        this.cleanFlagFiles();
    }

    @Override
    public void onAppConfig() {
        settingsController.showAsDialog(mainView);
    }

    // Add the views to this Frame
    private void initializeComponents() {
        try {
            // Main views
            mainView = new MainView();
            mainView.setController(this);
            // Init InputsView
            inputsView = new InputsView();
            inputsView.setController(this);
            inputsView.setEmpresaInfo (settingsController.getNickname (), settingsController.getUrlWeb());

            tabsPanel = mainView.createTabs();
            tabsPanel.addTab("Entradas:", inputsView);

            // Get components from views
            imageView = inputsView.getImageView();

        } catch (Exception ex) {
            JOptionPane.showMessageDialog(null, ex.getMessage());
            ex.printStackTrace();
        }
    }

    @Override
    public JFrame getMainView() {
        return mainView;
    }

    // Remove file flags used for controlling the global process (server and bot)
    @Override
    public void cleanFlagFiles() {
        try {
            Path exitFlagPath = Paths.get(DocModel.runningPath, DocModel.flagServerExitFilename);
            if (exitFlagPath.toFile().exists()) {
                Files.delete(exitFlagPath);
            }

            Path botStopFlagPath = Paths.get(DocModel.runningPath, DocModel.flagBotStopFilename);
            if (botStopFlagPath.toFile().exists()) {
                Files.delete(botStopFlagPath);
            }
        } catch (IOException ex) {
            Logger.getLogger(MainController.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    // Start document processing after button pressed in InpusView
    @Override
    public void onStartProcessing(String selectedFile, String empresa, String docType, String pais, String docNumber, String distrito) {
        docModel.currentRecord = new DocRecord(selectedFile, empresa, docType, docNumber);

        // Start resultsController
        if (resultsController != null) {
            tabsPanel.remove(resultsController.resultsView);
        }

        resultsController = new ResultsController(this, docModel);
        tabsPanel.addTab("Resultados", resultsController.resultsView);

        // Call to server to start processing documents
        String docFilepath = docModel.copyDocToProjectsDir(docModel.currentRecord);
        String[] params = {"doc_processing", docFilepath, empresa, pais, distrito};
        PythonWorker worker = new PythonWorker(this, params);
        worker.execute();

        // Shows a progress dialog while the process is running
        SwingUtilities.invokeLater(() -> {
            try {
                progressDialog = new ProgressDialog(this, mainView);
                progressDialog.startProcess();
            } catch (Exception e) {
            }
        });
    }

    // Selected docFile in  FileChooser or table from InputsFilesViewProjects
    @Override
    public void onFileSelectedPdf(File pdfFilepath) {
        try {
            String pdfFilepathStr = pdfFilepath.toString();
            DocModel.selectedFilePath = pdfFilepathStr;

            imageView.showImage(pdfFilepath);
            appCommander.getInitialPdfInfo(pdfFilepathStr, settingsController);

        } catch (Exception ex) {
            Logger.getLogger(MainController.class.getName()).log(Level.SEVERE, null, ex);
            JOptionPane.showMessageDialog(null, "Problemas seleccionando el documento PDF");
        }
    }

    @Override
    public void setInitialPdfInfo(Map<String, String> info) {
        inputsView.showDocInfo(info.get("docEmpresa"), info.get("docType"), info.get("docPais"), info.get("docNumber"));
        inputsView.enableProcessingButton(true);
    }

    // When user type docModel number instead of selecting file
    @Override
    public void onFileSelectedWeb(String dummyFilename) {
        inputsView.enableProcessingButton(true);
    }

    // Open PDF using system default viewer
    @Override
    public void onOpenPdfFile() {
        Utils.openPdfFile(DocModel.selectedFilePath);
    }
    
    // Message from TestEmpresaDialog
    @Override
    public void onTestingNewEmpresa(String empresa) {
        inputsView.showDocInfo(empresa);
    }

    // InputsView files selected by FileChooser
    // Send selected file to ready table
    // ServeWorker notification 
    @Override
    public void onEndProcessing(String statusMsg, String text) {
        try {
            if (statusMsg.contains("EXITO")) {
                out(">>> Documento procesado sin errores");
                String docFilepath = text.split("'")[1].trim();
                String jsonFilepath = Utils.getResultsFile(docFilepath, "ECUFIELDS.json");
                DocRecord docRecord = new DocRecord(docModel.currentRecord, docFilepath, jsonFilepath);
                docModel.currentRecord = docRecord;
                resultsController.setCurrentRecord(docRecord);
                tabsPanel.setSelectedIndex(1);
            } else {
                out(">>> Documento procesado con errores: " + text);
                TopMessageDialog.show(this.getMainView(), text);
                //String message = text.split("::", 2)[1].replace("\\", "\n");
            }
        } catch (ParseException | IOException ex) {
            ex.printStackTrace();
            out(ex.toString());

        } catch (Exception ex) {
            Logger.getLogger(MainController.class.getName()).log(Level.SEVERE, null, ex);
        } finally {
            if (progressDialog != null) {
                progressDialog.endProcess("document_processed");
            }
        }
    }

    // Stop cartaporte server if it was opened
    @Override
    public void onWindowClosing() {
        try {
            ClosingMessage.showClosingMessage("Applicación se está cerrando", this.mainView);
            String[] params = {"stop_application", null, null, null, null};
            PythonWorker worker = new PythonWorker(this, params);
            worker.execute();
            this.forcedExitWithTimer(1);
        } catch (Exception ex) {
            // ex.printStackTrace ();
            System.out.println("+++" + "Excepción de cierre de aplicación");
        }
    }
    
    @Override
    public void onNuevaActualizacion () {
        TopMessageDialog.show (this.getMainView(), "Existe una nueva actualización de EcuapassBot. Vuelva a iniciar.");
        this.onWindowClosing();
    }
//
//    // Notify commander that settings were updated
//    public void onSettingsSaved() {
//        appCommander.onSaveSettings();
//    }

    private void forcedExitWithTimer(int timeInSeconds) {
        timer = new Timer(timeInSeconds * 1000, new ActionListener() {  // Timer fires after 5 seconds
            @Override
            public void actionPerformed(ActionEvent e) {
                out("...Finalizado tiempo de salida forzada.");
                System.exit(0);
            }
        });
        timer.start(); // Start the timer
    }

    // Write message text to both: stdout and FeedbackView
    @Override
    public void out(String s) {
        System.out.println(s);
        this.settingsController.println(s);
    }

    public static void showClosingMessage(String message) {
        Thread thread = new Thread(() -> JOptionPane.showMessageDialog(null, message, "Closing Application", JOptionPane.INFORMATION_MESSAGE));
        thread.start();
    }

    @Override
    public void setWindowState(String state) {
        if (state.equals("minimize")) {
            mainView.setState(JFrame.ICONIFIED);
        } else if (state.equals("restore")) {
            mainView.setState(JFrame.NORMAL);
        }
    }

    // Send feedback to cloud
    @Override
    public void onSendFeedback(String feedbackText) {

        String zipFilepath = Utils.createTempCompressedFileFromText(feedbackText);
        // Call to server to start processing documents
        System.out.println("-- " + zipFilepath);
        //serverWorker.startProcess ("send_feedback", zipFilepath, docFilepath);
    }

    // Get app release from file "VERSION-XXX" in running path
    @Override
    public String getAppRelease() {
        String appRelease = Utils.getAppRelease(DocModel.runningPath);
        if (appRelease != null) {
            return appRelease;
        } else {
            return this.appRelease;
        }
    }

    @Override
    public void disableButtons() {
        this.inputsView.disableButtons();
    }

    public static void main(String args[]) {
        try {
            // Reset all UI defaults
            UIManager.getLookAndFeelDefaults().clear();
            UIManager.getDefaults().clear();

            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            // After setting system L&F
//			UIManager.put ("Button.background", Color.YELLOW);
//			UIManager.put ("Button.foreground", Color.BLACK);
//			UIManager.put ("Button.border", BorderFactory.createEmptyBorder (5, 15, 5, 15));

            // For all buttons to use custom bg
//			UIManager.addPropertyChangeListener (evt -> {
//				if ("lookAndFeel".equals (evt.getPropertyName ()))
//					UIManager.put ("Button.background", Color.YELLOW);
//			});
        } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(MainView.class
                    .getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        //</editor-fold>
        //  Create and display the form
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new MainController();
            }
        });

    }
}

class ClosingMessage {

    public static void showClosingMessage(String message, Component mainWindow) {
        Thread thread = new Thread(() -> JOptionPane.showMessageDialog(mainWindow, message, "Cerrando aplicación", JOptionPane.INFORMATION_MESSAGE));
        thread.start();
    }
}
