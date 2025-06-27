package results;

import documento.DocModel;
import main.Controller;
import widgets.ImageViewLens;
import java.awt.BorderLayout;
import widgets.ColorButton;

public class ResultsView extends javax.swing.JPanel {

	@SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        splitImage = new javax.swing.JSplitPane();
        imageView = new widgets.ImageViewLens();
        recordPanel = new javax.swing.JPanel();
        ecuapassView = new results.EcuapassView();
        transmitControlPanel = new javax.swing.JPanel();
        sendEcuapassButton = new ColorButton();
        sendCodebinButton = new javax.swing.JButton();
        sendEcuapassdocsButton = new javax.swing.JButton();

        setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));
        setLayout(new java.awt.BorderLayout());

        splitImage.setBackground(new java.awt.Color(204, 204, 255));
        splitImage.setMinimumSize(new java.awt.Dimension(100, 200));

        imageView.setMinimumSize(new java.awt.Dimension(200, 300));
        imageView.setPreferredSize(new java.awt.Dimension(400, 500));
        splitImage.setLeftComponent(imageView);

        recordPanel.setPreferredSize(new java.awt.Dimension(150, 37));
        recordPanel.setLayout(new java.awt.BorderLayout());
        recordPanel.add(ecuapassView, java.awt.BorderLayout.CENTER);

        transmitControlPanel.setBackground(new java.awt.Color(204, 204, 255));

        sendEcuapassButton.setBackground(new java.awt.Color(255, 255, 0));
        sendEcuapassButton.setText("Transmitir al ECUAPASS");
        sendEcuapassButton.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));
        sendEcuapassButton.setMargin(new java.awt.Insets(0, 10, 0, 10));
        sendEcuapassButton.setPreferredSize(new java.awt.Dimension(200, 50));
        sendEcuapassButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                sendEcuapassButtonActionPerformed(evt);
            }
        });
        transmitControlPanel.add(sendEcuapassButton);

        sendCodebinButton.setBackground(new java.awt.Color(153, 255, 153));
        sendCodebinButton.setText("<html>Transmitir al<br>CODEBIN</html>");
        sendCodebinButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                sendCodebinButtonActionPerformed(evt);
            }
        });
        transmitControlPanel.add(sendCodebinButton);

        sendEcuapassdocsButton.setBackground(new java.awt.Color(153, 255, 255));
        sendEcuapassdocsButton.setText("<html>Transmitir al<br>ECUAPASSDOCS</html>");
        sendEcuapassdocsButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                sendEcuapassdocsButtonActionPerformed(evt);
            }
        });
        transmitControlPanel.add(sendEcuapassdocsButton);

        recordPanel.add(transmitControlPanel, java.awt.BorderLayout.SOUTH);

        splitImage.setBottomComponent(recordPanel);

        add(splitImage, java.awt.BorderLayout.CENTER);
    }// </editor-fold>//GEN-END:initComponents

  private void sendEcuapassdocsButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_sendEcuapassdocsButtonActionPerformed
    controller.onBotSubmitToApp ("ECUAPASSDOCS");
  }//GEN-LAST:event_sendEcuapassdocsButtonActionPerformed

  private void sendCodebinButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_sendCodebinButtonActionPerformed
    controller.onBotSubmitToApp ("CODEBIN");
  }//GEN-LAST:event_sendCodebinButtonActionPerformed

  private void sendEcuapassButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_sendEcuapassButtonActionPerformed
    controller.onBotTransmit ();
  }//GEN-LAST:event_sendEcuapassButtonActionPerformed

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private results.EcuapassView ecuapassView;
    private widgets.ImageViewLens imageView;
    private javax.swing.JPanel recordPanel;
    private javax.swing.JButton sendCodebinButton;
    private javax.swing.JButton sendEcuapassButton;
    private javax.swing.JButton sendEcuapassdocsButton;
    private javax.swing.JSplitPane splitImage;
    private javax.swing.JPanel transmitControlPanel;
    // End of variables declaration//GEN-END:variables

	Controller controller;

	public ResultsView () {
		initComponents ();
		this.sendCodebinButton.setVisible (DocModel.SHOW_DOCS_BUTTONS);
		this.sendEcuapassdocsButton.setVisible (DocModel.SHOW_DOCS_BUTTONS);
	}

	public void setController (Controller controller) {
		this.controller = controller;
	}

	// 
	void setRecordView (EcuapassView recordView) {
		recordPanel.remove (this.ecuapassView);
		this.ecuapassView = recordView;
		this.ecuapassView.setController (controller);
		recordPanel.add (recordView, BorderLayout.CENTER);

		this.revalidate ();
	}

	public ImageViewLens getImageView () {
		return imageView;
	}
}
