package results;

import documento.DocModel;
import documento.DocRecord;
import java.awt.Frame;
import java.awt.Point;
import java.awt.Rectangle;
import widgets.ImageViewLens;
import main.Controller;
import main.Utils;
import java.io.File;
import java.io.FileNotFoundException;
import java.nio.file.Paths;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import widgets.BotControlDialog;
import widgets.TopMessageDialog;
import commander.PythonWorker;
import java.io.IOException;
import main.MainController;
import org.json.simple.parser.ParseException;

public class ResultsController extends Controller {

    Controller controller;
    DocModel docModel;
    DocRecord docRecord;
    EcuapassWarnings ecuapassWarnings;

    public ResultsView resultsView;
    EcuapassView ecuapassView;
    ImageViewLens imageView;
    BotControlDialog botDialog;

    public ResultsController(Controller controller, DocModel docModel) {
        this.controller = controller;
        this.docModel = docModel;
        this.docRecord = docModel.currentRecord;

        resultsView = new ResultsView();
        resultsView.setController(this);
        imageView = resultsView.getImageView();
        imageView.setController(controller);
    }

    public ResultsController(Controller controller, DocModel docModel, ResultsView resultsview) {
        this.controller = controller;
        this.docModel = docModel;
        this.docRecord = docModel.currentRecord;
        this.resultsView = resultsview;

        imageView = resultsView.getImageView();
    }

    @Override
    public JFrame getMainView() {
        return controller.getMainView();
    }

    public void setCurrentRecord(DocRecord docRecord) {
        this.showRecord(docRecord);
    }

    // Show document image and record into ResultsView
    public EcuapassWarnings showRecord(DocRecord docRecord) {
        try {
            File imgFile = new File(docRecord.docFilepath);
            imageView.showImage(imgFile);
            if (docRecord.docType.equals("CARTAPORTE")) {
                ecuapassView = new EcuapassViewCartaporte();
            } else if (docRecord.docType.equals("MANIFIESTO")) {
                ecuapassView = new EcuapassViewManifiesto();
            } else if (docRecord.docType.equals("DECLARACION")) {
                ecuapassView = new EcuapassViewDeclaracion();
            }

            resultsView.setRecordView(ecuapassView);

            // Set EcuapassWarnings
            ecuapassWarnings = ecuapassView.setDocRecord(docRecord);
            ecuapassWarnings.showWarnings(this.resultsView);
            return ecuapassWarnings;
        } catch (Exception ex) {
            Logger.getLogger(ResultsController.class.getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }

    // Doc transmission BUT before that: show warnings, update record.
    @Override
    public void onBotTransmit() {
        try {
            controller.cleanFlagFiles();
            // Update record with user changes
            this.docRecord = ecuapassView.getDocRecord();
            String ecuFieldsFilename = this.docRecord.getEcufieldsFile();
            this.docRecord.writeToJsonFile(ecuFieldsFilename);

            out("Inicio de digitación del documento...");
            String[] params = {"bot_init_transmission", DocModel.empresa, ecuFieldsFilename, docModel.runningPath, null};
            PythonWorker worker = new PythonWorker(this, params);
            worker.execute();
        } catch (FileNotFoundException ex) {
            JOptionPane.showMessageDialog(this.resultsView, "No hay documentos seleccionados para procesar!");
            return;
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(this.resultsView, "Problemas antes de transmitir el documento.");
            return;
        }
    }

    // Start bot typing to ECUAPASS
    @Override
    public void onBotStartTyping() {
        try {
            controller.cleanFlagFiles();
            String ecuFieldsFilename = docRecord.getEcufieldsFile();

            // Dialog stop button coordinates to confine mouse
            String stopButtonCoordsString = botDialog.stopButtonCoordsString;

            String[] params = {"bot_init_typing", DocModel.empresa, ecuFieldsFilename, docModel.runningPath, stopButtonCoordsString};
            PythonWorker worker = new PythonWorker(this, params);
            worker.execute();
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(this.resultsView, "Problemas transmitiendo el documento.");
            return;
        }
    }

    // Creates the stop flag so that the	server stop the typin process
    public void onBotCancelTyping() {
        String flagStopFilepath = Paths.get(docModel.runningPath, "flag-bot-stop.flag").toString();
        controller.out("+++ Canceling bot processing...");
        Utils.createEmptyFile(flagStopFilepath);
        //JOptionPane.showMessageDialog (this.resultsView, "Digitación cancelada.");
    }

    @Override
    public void onActivatedEcuapassWindow() {
        // Initialize BotControllerDialog
        botDialog = new BotControlDialog((Frame) null, true);
        botDialog.initialize(this, docRecord.getDocType());
        botDialog.setVisible(true);
    }

    // Send Bot Control Dialog coordinates to python commander		
    public void sendBotControlCoordinates(BotControlDialog botDialog) {
        Rectangle b = botDialog.getBounds();
        Point p = botDialog.getLocationOnScreen();

        String coordString = String.format("%s,%s,%s,%s", p.x, p.y, b.width, b.height);
        System.out.println("+++ Sending coordinates:" + coordString);
        String[] params = {"bot_control_coordinates", coordString, null, null};
        System.out.println("+++ Sending coordinates::params" + params);
        //PythonWorker worker = new PythonWorker (this, params);
        //worker.execute ();
    }

    public void showFinalProcessingMessage(String message) {
        this.controller.getMainView().setState(JFrame.ICONIFIED);
        if (botDialog != null) {
            botDialog.dispose();
        }
        TopMessageDialog dialog = new TopMessageDialog(controller.getMainView(), message);
    }

    // RunWorker notification
//    public void onTypedDocument(String msgStatus, String response) {
//        out(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
//        out(response);
//        out(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
//        if (botDialog != null) {
//            botDialog.dispose();
//        }
//        TopMessageDialog.show(this.getMainView(), response);
//    }

    @Override
    public void onEndProcessing(String statusMsg, String text) {
        try {
            TopMessageDialog.show(this.getMainView(), text);
        } catch (Exception ex) {
            Logger.getLogger(MainController.class.getName()).log(Level.SEVERE, null, ex);
        } finally {
            if (botDialog != null) {
                botDialog.dispose();
            }
        }
    }

    @Override
    public void onEcuapassWarningsResponse(String response) {
        System.out.println("+++" + "onEcuapassWarningsResponse NOT IMPLEMENTED");
    }

    @Override
    public void onOpenPdfFile() {
        controller.onOpenPdfFile();
    }

    @Override
    public void out(String text) {
        controller.out(text);
    }
}
