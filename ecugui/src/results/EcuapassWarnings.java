package results;

import documento.DocModel;
import static java.awt.Color.RED;
import java.awt.Component;
import java.awt.Font;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import main.Controller;
import main.Utils;
import commander.PythonWorker;

// Check for valid ecuapass values and set and store warnings
public class EcuapassWarnings {

	List<String[]> keyValueList;
	Controller controller;

	public EcuapassWarnings () {
		keyValueList = new ArrayList ();
	}

	public void setController (Controller controller) {
		this.controller = controller;
	}

	String checkAddValue (String key, String value, Component cmp) {
		if (value.contains ("||")) { // Check for confidence extraction
			String[] parts = value.split ("\\|\\|");
			String alertWord = parts[1];
			value = parts[0];
			//record.mainFields.replace (k, value);
			if (alertWord.equals ("LOW"))
				cmp.setBackground (Utils.LOW_RED);
			else if (alertWord.equals ("WARNING")) {
				cmp.setBackground (Utils.MID_YELLOW); cmp.setForeground (RED);
				cmp.setFont (new Font ("Arial", Font.BOLD, 12));
				String keyValue[] = {key, value};
				keyValueList.add (keyValue);
			} else if (alertWord.equals ("ERROR")) {
				cmp.setBackground (Utils.LOW_RED); cmp.setForeground (RED);
				cmp.setFont (new Font ("Arial", Font.BOLD, 12));
				String keyValue[] = {key, value};
				keyValueList.add (keyValue);
			} else if (alertWord.equals ("NEEDED"))
				cmp.setBackground (Utils.MID_YELLOW);
			else
				System.out.println (">>> PRECAUCION: Palabra de alerta desconocida: " + alertWord);
		}
		return value;
	}

	public String showWarnings (JPanel view) {
		if (keyValueList.isEmpty ())
			return null;
		
		String textWarnings = "<html>" + "Se cambiaron de formato los siguientes valores: <ul>";
		for (String[] kv : keyValueList) {
			textWarnings += "<li>" + kv[0] + " : " + kv[1] + "</li>";
		}
		textWarnings += "</ul>Revíselos y corríjalos en el ECUAPASS<br> </html>";

		// Show the custom JOptionPane
		Object[] options = {"Continuar"};
		int option = JOptionPane.showOptionDialog (view, textWarnings, "Precaución",
			JOptionPane.YES_NO_OPTION, JOptionPane.ERROR_MESSAGE, null,
			options, options[0]);
		if (option == 0)
			return "CORREGIR";
		//controller.onEcuapassWarningsResponse ("CORREGIR");
		else
			return "CONTINUAR";
		//controller.onEcuapassWarningsResponse ("CONTINUAR");			
	}
}
