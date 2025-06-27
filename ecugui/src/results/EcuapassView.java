package results;

import documento.DocModel;
import documento.DocRecord;
import java.awt.Component;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;
import javax.swing.JRadioButton;
import main.Controller;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.text.JTextComponent;
import main.Utils;
import widgets.SearchableComboBox;

public class EcuapassView extends JScrollPane {
	@SuppressWarnings("unchecked")
  // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
  private void initComponents() {

    setBorder(javax.swing.BorderFactory.createTitledBorder(null, "Documento:", javax.swing.border.TitledBorder.DEFAULT_JUSTIFICATION, javax.swing.border.TitledBorder.DEFAULT_POSITION, new java.awt.Font("DejaVu Sans", 1, 12), java.awt.Color.red)); // NOI18N
    setForeground(java.awt.Color.red);
  }// </editor-fold>//GEN-END:initComponents

  // Variables declaration - do not modify//GEN-BEGIN:variables
  // End of variables declaration//GEN-END:variables

	public Controller controller;
	public DocRecord docRecord;
	public EcuapassPanel ecuapassPanel;
	public String resourcesDir;

	public EcuapassView () {
		initComponents ();
	}

	public void setController (Controller controller) {
		this.controller = controller;
	}

	// Set and Show document docRecord on Ecuapass view. It also checks warnings
	public EcuapassWarnings setDocRecord (DocRecord record) {
		this.docRecord = record;
		String filename = record.docType + "  :  " + record.docTypeFilename;
	    setBorder(javax.swing.BorderFactory.createTitledBorder (null, filename, javax.swing.border.TitledBorder.CENTER, javax.swing.border.TitledBorder.CENTER, new java.awt.Font("DejaVu Sans", 1, 14), java.awt.Color.blue)); // NOI18N
	
		// Show docRecord on view
		Object[] mainKeys = record.getMainKeysSorted ().toArray ();
		Component[] fields = ecuapassPanel.getComponents ();

		EcuapassWarnings watnings = new EcuapassWarnings ();
		for (int i = 0; i < mainKeys.length; i++) {
			String key = (String) mainKeys[i];
			String value = (String) record.mainFields.get (key);
			Component cmp = fields[i];
			if (value.equals (""))	
				continue;
			
			// Check if valid value and set warning color
			value = watnings.checkAddValue (key, value, cmp);

			// Show the value in the component
			if (cmp instanceof JTextComponent) {
				JTextComponent textComponent = (JTextComponent) cmp;
				textComponent.setText (value);
			} else if (cmp instanceof JScrollPane) {
				JTextArea textComponent = (JTextArea) ((JScrollPane) cmp).getViewport ().getView ();
				textComponent.setText (value);
			} else if (cmp instanceof SearchableComboBox) {
				SearchableComboBox comboBox = (SearchableComboBox) cmp;
				comboBox.selectItemFromSubstring (value);
			}else if (cmp instanceof JRadioButton) {
				JRadioButton rb = (JRadioButton) cmp;
				rb.doClick ();
			} else
				System.out.println (">>> NOT JTextComp: " + cmp.getClass ());
		}
		return watnings;
	}
	
	// After user updates ECUAPASS form
	// Update docRecord values from text in components
	public DocRecord getDocRecord () {
		Object[] mainKeys = docRecord.getMainKeysSorted ().toArray ();
		Component[] fields = ecuapassPanel.getComponents ();

		for (int i = 0; i < mainKeys.length; i++) {
			String key = (String) mainKeys[i];
			Component cmp = fields[i];

			if (cmp instanceof JTextComponent) {
				JTextComponent textComponent = (JTextComponent) cmp;
				String text = textComponent.getText ();
				docRecord.update (key, text);
			} else if (cmp instanceof JScrollPane) {
				JTextArea textComponent = (JTextArea) ((JScrollPane) cmp).getViewport ().getView ();
				String text = textComponent.getText ();
				docRecord.update (key, text);
			} else if (cmp instanceof SearchableComboBox) {
				SearchableComboBox comboBox = (SearchableComboBox) cmp;
				String textAll = (String) comboBox.getSelectedItem ();
				String text = "";
				if (textAll.contains ("--Selección--") == false)
					text = textAll.split ("\\s+", 2)[1];          // Ecuapass data stasts with [###]

				docRecord.update (key, text);
			} else
				System.out.println (">>> NOT JTextComp: " + cmp.getClass ());
		}
		return docRecord;
	}

//	public void setDocRecord (DocRecord docRecord) {
//		this.docRecord = docRecord;
//		String filename = docRecord.docType + "  :  " + docRecord.docTypeFilename;
//	    setBorder(javax.swing.BorderFactory.createTitledBorder (null, filename, javax.swing.border.TitledBorder.CENTER, javax.swing.border.TitledBorder.CENTER, new java.awt.Font("DejaVu Sans", 1, 14), java.awt.Color.blue)); // NOI18N
//	}

	// For idependent combo box
	public SearchableComboBox createComboBox (String filename) {
		//String resourcesFile = Paths.get (DocModel.temporalPath, "resources", this.resourcesDir, filename + ".txt").toString ();
		String resourcesFile = Paths.get (DocModel.resourcesPath, this.resourcesDir, filename + ".txt").toString ();
		String[] items = Utils.readDataFromFile (resourcesFile);
		SearchableComboBox comboBox = new SearchableComboBox (items);
		return (comboBox);
	}

	// For dependent combo box (e.g. "ciudades" depends of "paises")
	// Loads all dependent files (e.g. "ciudades" for each "pais")
	public SearchableComboBox createComboBox (String filename, SearchableComboBox parentComboBox) {
		Map<String, String[]> subItemsMap = new HashMap<> ();
		String childName = filename.split ("_")[1];
		String[] rootItems = null;
		if (childName.equals ("ciudades"))
			rootItems = new String[]{"COLOMBIA", "ECUADOR", "PERU","VENEZUELA","derivado"};
		else if (childName.equals ("depositos"))
			rootItems = new String[]{"QUITO", "TULCAN", "HUAQUILLAS", "HUAQUILLAS", "LOJA", "CEBAF", "derivado"};
		else if (childName.equals ("aduanas"))
			rootItems = new String[]{"COLOMBIA", "ECUADOR", "PERU", "VENEZUELA", "derivado"};
		else
			System.out.println (">>> ALERTA: Tipo de items de ComboBox desconocido:" + childName);

		if (rootItems != null)
			for (String rootItem : rootItems) {
				String itemFilename = rootItem.contains ("derivado") ? "derivado" : childName + "_" + rootItem.toLowerCase ();
				//String resourcesFile = Paths.get (DocModel.temporalPath, "resources", this.resourcesDir, itemFilename + ".txt").toString ();
				String resourcesFile = Paths.get (DocModel.resourcesPath, this.resourcesDir, itemFilename + ".txt").toString ();
				String[] items = Utils.readDataFromFile (resourcesFile);
				subItemsMap.put (rootItem, items);
			}
		//String resourcesFile = Paths.get (DocModel.temporalPath, "resources", this.resourcesDir, "derivado.txt").toString ();
		String resourcesFile = Paths.get (DocModel.resourcesPath, this.resourcesDir, "derivado.txt").toString ();
		String[] items = Utils.readDataFromFile (resourcesFile);
		SearchableComboBox comboBox = new SearchableComboBox (items, parentComboBox, subItemsMap);
		return (comboBox);
	}
}