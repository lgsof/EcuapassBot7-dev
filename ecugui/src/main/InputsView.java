package main;

import java.awt.Component;
import java.awt.KeyboardFocusManager;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.event.InputEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.File;
import java.util.prefs.Preferences;
import javax.swing.JFileChooser;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.Timer;
import javax.swing.UIManager;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.TableColumnModel;
import widgets.ImageViewLens;
import widgets.TestEmpresasDialog;
import main.Controller;
import settings.SettingsController;

public class InputsView extends javax.swing.JPanel {

    @SuppressWarnings("unchecked")
  // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
  private void initComponents() {

    filesPanel = new javax.swing.JPanel();
    docInputPanel = new widgets.DocumentInputPanel();
    selectionPanel = new javax.swing.JPanel();
    fileChooser = new javax.swing.JFileChooser();
    imageView = new widgets.ImageViewLens();

    setPreferredSize(new java.awt.Dimension(800, 500));
    setLayout(new java.awt.BorderLayout());

    filesPanel.setPreferredSize(new java.awt.Dimension(600, 800));
    filesPanel.setLayout(new javax.swing.BoxLayout(filesPanel, javax.swing.BoxLayout.Y_AXIS));

    docInputPanel.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));
    docInputPanel.setMaximumSize(new java.awt.Dimension(2147483647, 170));
    docInputPanel.setMinimumSize(new java.awt.Dimension(521, 170));
    docInputPanel.setPreferredSize(new java.awt.Dimension(700, 170));
    filesPanel.add(docInputPanel);

    selectionPanel.setPreferredSize(new java.awt.Dimension(580, 700));
    selectionPanel.setLayout(new java.awt.BorderLayout());

    fileChooser.setBackground(new java.awt.Color(204, 255, 204));
    fileChooser.setControlButtonsAreShown(false);
    fileChooser.setAlignmentY(0.1F);
    fileChooser.setAutoscrolls(true);
    fileChooser.setBorder(javax.swing.BorderFactory.createTitledBorder("Selección de facturas:"));
    fileChooser.setMinimumSize(new java.awt.Dimension(442, 200));
    selectionPanel.add(fileChooser, java.awt.BorderLayout.CENTER);

    filesPanel.add(selectionPanel);

    add(filesPanel, java.awt.BorderLayout.WEST);

    imageView.setBackground(java.awt.Color.orange);
    imageView.setMaximumSize(new java.awt.Dimension(600, 800));
    add(imageView, java.awt.BorderLayout.CENTER);
  }// </editor-fold>//GEN-END:initComponents

    // NEW: docInputPanel
    public void onStartProcessing(String selectedFile, String empresa, String docType, String pais, String numero, String distrito) {
        controller.onStartProcessing(selectedFile, empresa, docType, pais, numero, distrito);
    }

  // Variables declaration - do not modify//GEN-BEGIN:variables
  private widgets.DocumentInputPanel docInputPanel;
  private javax.swing.JFileChooser fileChooser;
  private javax.swing.JPanel filesPanel;
  private widgets.ImageViewLens imageView;
  private javax.swing.JPanel selectionPanel;
  // End of variables declaration//GEN-END:variables

    Controller controller;
    String selectedFile = null;
    private static boolean isCtrlPressed = false;

    // Preferences key to store the last used directory
    private static final String LAST_USED_DIR_KEY = "lastUsedDirectory";

    public InputsView() {
        initComponents();
        modifyFileChooser();
    }

    public void setController(Controller controller) {
        this.controller = controller;
        this.docInputPanel.setController(this);
        this.imageView.setController(controller);
        addFileChooserListeners();
        fileChooser.setSelectedFile(null);
    }

    public void setEmpresaInfo(String nickname, String urlWeb) {
        this.docInputPanel.showDocInfo(nickname, "", "", "");
        // Disable editing for 'empresas' with not URL
        if (urlWeb.isEmpty()) {
            this.docInputPanel.setEditable(false);
        }
    }

    public void addFileChooserListeners() {
        // Add listener for file selection (for preview)
        fileChooser.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentShown(ComponentEvent e) {
                resizeColumns(fileChooser);
            }
        });

        fileChooser.addPropertyChangeListener(new PropertyChangeListener() {
            @Override
            public void propertyChange(PropertyChangeEvent evt) {
                if (JFileChooser.SELECTED_FILE_CHANGED_PROPERTY.equals(evt.getPropertyName())) {
                    File selectedFile = fileChooser.getSelectedFile();
                    if (selectedFile != null && !selectedFile.isDirectory()) {
                        onFileSelectedPdf(selectedFile);
                        updateLastDirectoryUsed(selectedFile);
                    }
                }
            }
        });

        // Track Ctrl key pressed
        // Use KeyboardFocusManager to track global key events
        KeyboardFocusManager.getCurrentKeyboardFocusManager().addKeyEventDispatcher(e -> {
            boolean ctrl = (e.getModifiersEx() & InputEvent.CTRL_DOWN_MASK) != 0;
            boolean shift = (e.getModifiersEx() & InputEvent.SHIFT_DOWN_MASK) != 0;
            boolean alt = (e.getModifiersEx() & InputEvent.ALT_DOWN_MASK) != 0;
            // Check for 'P' key
            if (e.getID() == KeyEvent.KEY_PRESSED && ctrl && shift && alt && e.getKeyCode() == KeyEvent.VK_P) {
                showTestEmpresasDialog();
            } else if (e.getID() == KeyEvent.KEY_PRESSED && e.getKeyCode() == KeyEvent.VK_CONTROL) {
                if (!isCtrlPressed) {
                    isCtrlPressed = true;
                }
            } else if (e.getID() == KeyEvent.KEY_RELEASED && e.getKeyCode() == KeyEvent.VK_CONTROL) {
                if (isCtrlPressed) {
                    isCtrlPressed = false;
                }
            }
            return false; // Ensure other components can process the event
        });

        // Add a timer to refres dir content
        Timer timer = new Timer(5000, new ActionListener() { // Update every 5 seconds
            @Override
            public void actionPerformed(ActionEvent e) {
                fileChooser.rescanCurrentDirectory();
            }
        });
        timer.start();
    }

    private void resizeColumns(JFileChooser chooser) {
        Component c = chooser.getComponent(0);
        if (c instanceof JPanel) {
            Component[] comps = ((JPanel) c).getComponents();
            for (Component comp : comps) {
                if (comp instanceof JScrollPane) {
                    JScrollPane scrollPane = (JScrollPane) comp;
                    Component view = scrollPane.getViewport().getView();
                    if (view instanceof JTable) {
                        JTable table = (JTable) view;
                        table.setAutoResizeMode(JTable.AUTO_RESIZE_LAST_COLUMN);

                        int totalWidth = table.getWidth();
                        TableColumnModel model = table.getColumnModel();

                        // Distribute width (adjust ratios as needed)
                        model.getColumn(0).setPreferredWidth((int) (totalWidth * 0.5)); // Name
                        model.getColumn(1).setPreferredWidth((int) (totalWidth * 0.15)); // Size
                        model.getColumn(2).setPreferredWidth((int) (totalWidth * 0.15)); // Type
                        model.getColumn(3).setPreferredWidth((int) (totalWidth * 0.2)); // Modified
                    }
                }
            }
        }
    }

    // Event from FileChooser
    public void onFileSelectedPdf(File selectedFile) {
        this.selectedFile = selectedFile.toString();
        docInputPanel.setSelectedFile(this.selectedFile);
        controller.onFileSelectedPdf(selectedFile);
    }

    // NEW: sent from docInputPanel
    public void onFileSelectedWeb(String dummyFilename) {
        controller.onFileSelectedWeb(dummyFilename);
    }

    // NEW: get docNumber from docInputPanel
    public String getDocNumber() {
        return docInputPanel.getDocNumber();
    }

    public void showDocInfo(String docEmpresa) {
        this.docInputPanel.showDocInfo(docEmpresa);
    }

    public void showDocInfo(String docEmpresa, String docType, String docPais, String docNumber) {
        this.clearDocInfo();
        this.docInputPanel.showDocInfo(docEmpresa, docType, docPais, docNumber);
    }

    public void clearDocInfo() {
        this.docInputPanel.clearDocInfo();
    }

    void updateLastDirectoryUsed(File selectedFile) {
        Preferences prefs = Preferences.userNodeForPackage(InputsView.class);
        String selectedDir = selectedFile.getParent();
        prefs.put(LAST_USED_DIR_KEY, selectedDir);
    }

    private void modifyFileChooser() {
        // Changes FileChooser text from english to spanish 
        UIManager.put("FileChooser.fileNameLabelText", "Archivos");
        UIManager.put("FileChooser.filesOfTypeLabelText", "Tipos de Archivos");
        UIManager.put("FileChooser.cancelButtonText", "Deseleccionar ");
        UIManager.put("FileChooser.openButtonText", "Seleccionar ");
        UIManager.put("FileChooser.lookInLabelText", "Buscar");

        UIManager.put("FileChooser.readOnly", Boolean.TRUE);
        fileChooser.updateUI();

        // Show only images and pdfs  in FileChooser
        fileChooser.setAcceptAllFileFilterUsed(false);
        FileNameExtensionFilter filter = new FileNameExtensionFilter("Images/pdf files", "jpg", "png", "pdf");
        fileChooser.addChoosableFileFilter(filter);

        // Hide default accept/cancel buttons
        hideFileSelComponents(fileChooser.getComponents());

        // Init to last used directory from preferences
        Preferences prefs = Preferences.userNodeForPackage(InputsView.class);
        String lastUsedDir = prefs.get(LAST_USED_DIR_KEY, null);
        if (lastUsedDir == null) {
            lastUsedDir = AppPrefs.FileLocation.get(System.getProperty("user.home"));
        }

        fileChooser.setCurrentDirectory(new File(lastUsedDir));
    }

    // Hide last file panel from JFileChooser component
    private void hideFileSelComponents(Component[] components) {
        // traverse through the components
        for (int i = 0; i < components.length; i++) {
            Component comp = components[i];
            if (comp instanceof JPanel) // traverse recursively
            {
                hideFileSelComponents(((JPanel) comp).getComponents());
            } else if (comp.toString().contains("Archivos")) {
                comp.getParent().getParent().setVisible(false); // hide i
            }
        }
    }

    public ImageViewLens getImageView() {
        return (imageView);
    }

    public void enableProcessingButton(boolean value) {
        docInputPanel.enableProcessButton(value);
    }

    // Create and display the dialog
    public void showTestEmpresasDialog() {
        TestEmpresasDialog testDialog = new TestEmpresasDialog(new javax.swing.JFrame(), true);
        testDialog.setController(controller);
        testDialog.addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent e) {
                testDialog.dispose();
            }
        });
        testDialog.setVisible(true);
    }

    public void disableButtons() {
        this.docInputPanel.disableButtons();
    }
}
