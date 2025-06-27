package widgets;

import java.awt.Font;
import java.awt.FontFormatException;
import java.awt.GraphicsEnvironment;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.io.InputStream;
import java.util.prefs.Preferences;
import javax.swing.JOptionPane;
import javax.swing.JRadioButton;
import javax.swing.JButton;
import javax.swing.text.AbstractDocument;
import main.InputsView;
import main.Utils;
import widgets.UppercaseDocumentFilter;

public class DocumentInputPanel extends javax.swing.JPanel {

    InputsView controller;
    String selectedFile;

    public DocumentInputPanel() {
        initComponents();
        this.addRButtonListeners();
        initDocNumberDocTypeField();
        this.setDocNumberFont();
        this.processButton.setEnabled(false);
    }

    public void setController(InputsView controller) {
        this.controller = controller;
    }

    public void setEditable(boolean editableFlag) {
        this.docNumberTXT.setEditable(editableFlag);
    }

    // Load custom font from the .ttf file and set to docNumber input field
    public void setDocNumberFont() {
        try {
            InputStream fontStream = getClass().getResourceAsStream("/resources/fonts/RobotoMono-Regular.ttf");
            Font customFont = Font.createFont(Font.TRUETYPE_FONT, fontStream).deriveFont(24f);
            GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
            ge.registerFont(customFont);
            this.docNumberTXT.setFont(customFont);
        } catch (FontFormatException | IOException e) {
            e.printStackTrace();
        }
    }

    public void showDocInfo(String docEmpresa) {
        this.setEmpresa(docEmpresa);
    }

    public void showDocInfo(String docEmpresa, String docType, String docPais, String docNumber) {
        this.setEmpresa(docEmpresa);
        this.setDocPais(docPais);
        this.setDocNumber(docNumber);
        this.setDocType(docType);
        this.getLastUsedDistrito();
    }

    public void clearDocInfo() {
        //this.empresaLBL.setText ("");
        this.setDocPais("");
        this.setDocNumber("");
        this.setDocType("");
    }

    // Add ActionListeners to the radio buttons
    public void addRButtonListeners() {
        ActionListener docTypeListener = new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String docNumber = getDocNumber();
                String docType = getDocType();
                String dummyFilename = Utils.createDummyFile(docNumber, docType);
                controller.onFileSelectedWeb(dummyFilename);
                selectedFile = dummyFilename;
                JRadioButton[] radioButtons = {cartaporteRB, manifiestoRB};
                Utils.toggleRadioButtonColor(radioButtons);
            }
        };
        cartaporteRB.addActionListener(docTypeListener);
        manifiestoRB.addActionListener(docTypeListener);

        ActionListener distritoListener = new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String distrito = getDocDistrito();
                updateLastUsedDistrito(distrito);
                JRadioButton[] radioButtons = {tulcanRB, huaquillasRB};
                Utils.toggleRadioButtonColor(radioButtons);
            }
        };
        tulcanRB.addActionListener(distritoListener);
        huaquillasRB.addActionListener(distritoListener);
    }

    // DocNumber functions
    private void initDocNumberDocTypeField() {
        ((AbstractDocument) docNumberTXT.getDocument()).setDocumentFilter(new UppercaseDocumentFilter());
    }

    public void setSelectedFile(String selectedFile) {
        this.selectedFile = selectedFile;
    }

    public void enableProcessButton(boolean value) {
        if (!this.docNumberTXT.getText().trim().equals("")) {
            this.processButton.setEnabled(value);
        }
    }

    public String getEmpresa() {
        return empresaLBL.getText();
    }

    public void setEmpresa(String empresa) {
        this.empresaLBL.setText(empresa);
    }

    public void setDocNumber(String numero) {
        this.docNumberTXT.setText(numero);
    }

    public String getDocNumber() {
        String docNumber = this.docNumberTXT.getText();
        if (docNumber.equals("")) {
            JOptionPane.showMessageDialog(this, "Número documento: " + docNumber + " inválido.");
            return null;
        }
        return docNumber;
    }

    public String getDocType() {
        if (this.cartaporteRB.isSelected()) {
            return "CARTAPORTE";
        } else if (this.manifiestoRB.isSelected()) {
            return "MANIFIESTO";
        } else {
            return null;
        }
    }

    public void setDocType(String docType) {
        if (docType.equals("CARTAPORTE")) {
            this.cartaporteRB.setSelected(true);
        } else if (docType.equals("MANIFIESTO")) {
            this.manifiestoRB.setSelected(true);
        } else if (docType == null || docType.equals("")) {
            this.docTypeBTG.clearSelection();
        }

        JRadioButton[] radioButtons = {cartaporteRB, manifiestoRB};
        Utils.toggleRadioButtonColor(radioButtons);
    }

    public String getDocDistrito() {
        if (this.tulcanRB.isSelected()) {
            return "TULCAN";
        } else if (this.huaquillasRB.isSelected()) {
            return "HUAQUILLAS";
        } else {
            return null;
        }
    }

    public void setDocDistrito(String distrito) {
        if (distrito.equals("TULCAN")) {
            this.tulcanRB.setSelected(true);
        } else if (distrito.equals("HUAQUILLAS")) {
            this.huaquillasRB.setSelected(true);
        } else if (distrito.equals("")) {
            this.distritoBTG.clearSelection();
        }

        JRadioButton[] radioButtons = {tulcanRB, huaquillasRB};
        Utils.toggleRadioButtonColor(radioButtons);
        this.updateLastUsedDistrito(distrito);
    }

    void updateLastUsedDistrito(String distrito) {
        Preferences prefs = Preferences.userNodeForPackage(InputsView.class);
        prefs.put("LastUsedDistrito", distrito);
    }

    String getLastUsedDistrito() {
        Preferences prefs = Preferences.userNodeForPackage(InputsView.class);
        String lastUsedDistrito = prefs.get("LastUsedDistrito", "TULCAN");
        this.setDocDistrito(lastUsedDistrito);
        return lastUsedDistrito;
    }

    public String getDocPais() {
        return this.paisTXT.getText();
    }

    public void setDocPais(String pais) {
        this.paisTXT.setText(pais);
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {
        java.awt.GridBagConstraints gridBagConstraints;

        docTypeBTG = new javax.swing.ButtonGroup();
        distritoBTG = new javax.swing.ButtonGroup();
        inputPanel = new javax.swing.JPanel();
        empresaLBL = new javax.swing.JLabel();
        docNumberTXT = new javax.swing.JTextField();
        processButton = new ColorButton();
        panelTipo = new javax.swing.JPanel();
        cartaporteRB = new javax.swing.JRadioButton();
        manifiestoRB = new javax.swing.JRadioButton();
        instructionLabel = new javax.swing.JLabel();
        panelPais = new javax.swing.JPanel();
        paisTXT = new javax.swing.JLabel();
        panelDistrito = new javax.swing.JPanel();
        tulcanRB = new javax.swing.JRadioButton();
        huaquillasRB = new javax.swing.JRadioButton();

        setBackground(new java.awt.Color(204, 255, 204));
        setMaximumSize(new java.awt.Dimension(2147483647, 120));
        setMinimumSize(new java.awt.Dimension(417, 120));
        setPreferredSize(new java.awt.Dimension(720, 120));
        setLayout(new java.awt.BorderLayout());

        inputPanel.setBackground(new java.awt.Color(204, 255, 204));
        inputPanel.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));
        inputPanel.setMaximumSize(new java.awt.Dimension(300, 200));
        inputPanel.setMinimumSize(new java.awt.Dimension(342, 200));
        inputPanel.setPreferredSize(new java.awt.Dimension(382, 200));
        inputPanel.setLayout(new java.awt.GridBagLayout());

        empresaLBL.setBackground(new java.awt.Color(255, 255, 153));
        empresaLBL.setFont(new java.awt.Font("DejaVu Sans", 0, 18)); // NOI18N
        empresaLBL.setForeground(new java.awt.Color(0, 51, 255));
        empresaLBL.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        empresaLBL.setText("Empresa");
        empresaLBL.setBorder(null);
        empresaLBL.setMinimumSize(new java.awt.Dimension(2, 30));
        empresaLBL.setOpaque(true);
        empresaLBL.setPreferredSize(new java.awt.Dimension(44, 30));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.gridwidth = 3;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        inputPanel.add(empresaLBL, gridBagConstraints);

        docNumberTXT.setFont(new java.awt.Font("DejaVu Sans Mono", 0, 24)); // NOI18N
        docNumberTXT.setForeground(new java.awt.Color(0, 0, 255));
        docNumberTXT.setHorizontalAlignment(javax.swing.JTextField.CENTER);
        docNumberTXT.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));
        docNumberTXT.setMaximumSize(new java.awt.Dimension(100, 30));
        docNumberTXT.setMinimumSize(new java.awt.Dimension(100, 30));
        docNumberTXT.setPreferredSize(new java.awt.Dimension(120, 30));
        docNumberTXT.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyTyped(java.awt.event.KeyEvent evt) {
                docNumberTXTKeyTyped(evt);
            }
        });
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.gridwidth = 3;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        inputPanel.add(docNumberTXT, gridBagConstraints);

        processButton.setBackground(new java.awt.Color(255, 255, 0));
        processButton.setText("Procesar");
        processButton.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));
        processButton.setHorizontalTextPosition(javax.swing.SwingConstants.CENTER);
        processButton.setMaximumSize(new java.awt.Dimension(100, 30));
        processButton.setMinimumSize(new java.awt.Dimension(100, 30));
        processButton.setPreferredSize(new java.awt.Dimension(100, 30));
        processButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                processButtonActionPerformed(evt);
            }
        });
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 4;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 10);
        inputPanel.add(processButton, gridBagConstraints);

        panelTipo.setBorder(javax.swing.BorderFactory.createTitledBorder("Tipo:"));
        panelTipo.setPreferredSize(new java.awt.Dimension(120, 77));
        panelTipo.setLayout(new javax.swing.BoxLayout(panelTipo, javax.swing.BoxLayout.Y_AXIS));

        docTypeBTG.add(cartaporteRB);
        cartaporteRB.setText("CartaPorte");
        cartaporteRB.setHorizontalAlignment(javax.swing.SwingConstants.LEFT);
        cartaporteRB.setOpaque(true);
        panelTipo.add(cartaporteRB);

        docTypeBTG.add(manifiestoRB);
        manifiestoRB.setText("Manifiesto");
        manifiestoRB.setOpaque(true);
        panelTipo.add(manifiestoRB);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 2;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        inputPanel.add(panelTipo, gridBagConstraints);

        instructionLabel.setText("<html>Número de documento:</html>");
        instructionLabel.setOpaque(true);
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.insets = new java.awt.Insets(0, 0, 0, 10);
        inputPanel.add(instructionLabel, gridBagConstraints);

        panelPais.setBorder(javax.swing.BorderFactory.createTitledBorder("País:"));
        panelPais.setMinimumSize(new java.awt.Dimension(120, 66));
        panelPais.setPreferredSize(new java.awt.Dimension(120, 66));

        paisTXT.setForeground(java.awt.Color.blue);
        paisTXT.setText("País");
        panelPais.add(paisTXT);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 2;
        gridBagConstraints.gridy = 2;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        inputPanel.add(panelPais, gridBagConstraints);

        panelDistrito.setBorder(javax.swing.BorderFactory.createTitledBorder("Distrito:"));
        panelDistrito.setMaximumSize(new java.awt.Dimension(120, 77));
        panelDistrito.setMinimumSize(new java.awt.Dimension(120, 77));
        panelDistrito.setPreferredSize(new java.awt.Dimension(120, 77));
        panelDistrito.setLayout(new javax.swing.BoxLayout(panelDistrito, javax.swing.BoxLayout.Y_AXIS));

        distritoBTG.add(tulcanRB);
        tulcanRB.setText("Tulcán");
        tulcanRB.setOpaque(true);
        panelDistrito.add(tulcanRB);

        distritoBTG.add(huaquillasRB);
        huaquillasRB.setText("Huaquillas");
        huaquillasRB.setOpaque(true);
        panelDistrito.add(huaquillasRB);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 2;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        inputPanel.add(panelDistrito, gridBagConstraints);

        add(inputPanel, java.awt.BorderLayout.CENTER);
    }// </editor-fold>//GEN-END:initComponents

  private void docNumberTXTKeyTyped(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_docNumberTXTKeyTyped
      this.docTypeBTG.clearSelection();
      JRadioButton[] radioButtons = {cartaporteRB, manifiestoRB};
      Utils.toggleRadioButtonColor(radioButtons);
      this.processButton.setEnabled(false);
      String docNumber = docNumberTXT.getText();
      if (docNumber.startsWith("EC"))
          paisTXT.setText("ECUADOR");
      else if (docNumber.startsWith("CO"))
          paisTXT.setText("COLOMBIA");
      else if (docNumber.startsWith("PE"))
          paisTXT.setText("PERU");
      else
          paisTXT.setText("");
  }//GEN-LAST:event_docNumberTXTKeyTyped

  private void processButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_processButtonActionPerformed
      // TODO add your handling code here:
      String empresa = this.getEmpresa();
      String pais = this.getDocPais();
      String docNumber = this.getDocNumber();
      String docType = this.getDocType();
      String distrito = this.getDocDistrito();
      if (docNumber == null || docType == null) {
          return;
      }

      controller.onStartProcessing(selectedFile, empresa, docType, pais, docNumber, distrito);
  }//GEN-LAST:event_processButtonActionPerformed

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JRadioButton cartaporteRB;
    private javax.swing.ButtonGroup distritoBTG;
    private javax.swing.JTextField docNumberTXT;
    private javax.swing.ButtonGroup docTypeBTG;
    private javax.swing.JLabel empresaLBL;
    private javax.swing.JRadioButton huaquillasRB;
    private javax.swing.JPanel inputPanel;
    private javax.swing.JLabel instructionLabel;
    private javax.swing.JRadioButton manifiestoRB;
    private javax.swing.JLabel paisTXT;
    private javax.swing.JPanel panelDistrito;
    private javax.swing.JPanel panelPais;
    private javax.swing.JPanel panelTipo;
    private javax.swing.JButton processButton;
    private javax.swing.JRadioButton tulcanRB;
    // End of variables declaration//GEN-END:variables

    public void disableButtons() {
        this.processButton.setEnabled(false);
    }

    public void enableButtons() {
        if (!this.docNumberTXT.getText().trim().equals("")) {
            this.processButton.setEnabled(true);
        }
    }
}
