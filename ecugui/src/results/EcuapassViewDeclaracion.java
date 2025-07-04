package results;

import documento.DocModel;
import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import java.net.URL;
import java.util.ArrayList;
import javax.swing.ButtonGroup;
import javax.swing.JFrame;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import widgets.SearchableComboBox;

public class EcuapassViewDeclaracion extends EcuapassView {
	public EcuapassViewDeclaracion () {
		super ();
		resourcesDir = "/data_ecuapass/";
		URL imgPath = getClass().getResource("/resources/images/image-declaracion-ecuapass.png");
		ecuapassPanel = new EcuapassPanel (imgPath);
		Dimension size = new Dimension (967, 2150);
		ecuapassPanel.setPreferredSize (size);
		//setMaximumSize (size);
		setViewportView (ecuapassPanel);
		
		
		// Add panel's input fields
		ArrayList <Component> inputFields = getInputTextFields ();
		ecuapassPanel.addFields (inputFields);		
	}


	public static void main (String[] args) {
		DocModel doc = new DocModel ();
		doc.initGlobalPaths ();
		
		SwingUtilities.invokeLater (() -> {
			JFrame frame = new JFrame ("Custom JScrollPane Example");
			frame.getContentPane ().setLayout (new BorderLayout ());
			frame.setDefaultCloseOperation (JFrame.EXIT_ON_CLOSE);

			EcuapassViewDeclaracion sp = new EcuapassViewDeclaracion ();

			frame.getContentPane ().add (sp, BorderLayout.CENTER);
			frame.setPreferredSize (new Dimension (1000, 600));
			frame.pack ();
			frame.setVisible (true);
		});
	}

	
	public ArrayList <Component> getInputTextFields () {
		ArrayList <Component> imagePanel = new ArrayList <> ();
		SearchableComboBox txt01 = createComboBox ("distritos");imagePanel.add (txt01);txt01.setBounds (204, 103, 280, 18);
		JTextField txt02 = new JTextField ();imagePanel.add (txt02);txt02.setBounds (687, 103, 78, 18);
		SearchableComboBox txt03 = createComboBox ("procedimientos");imagePanel.add (txt03);txt03.setBounds (204, 126, 280, 18);
		JTextField txt04 = new JTextField ();imagePanel.add (txt04);txt04.setBounds (204, 149, 280, 18);
		SearchableComboBox txt05 = createComboBox ("paises");imagePanel.add (txt05);txt05.setBounds (687, 149, 280, 18);
		SearchableComboBox txt06 = createComboBox ("paises");imagePanel.add (txt06);txt06.setBounds (204, 172, 280, 18);
		SearchableComboBox txt07 = createComboBox ("derivado_aduanas", txt06);imagePanel.add (txt07);txt07.setBounds (687, 172, 280, 18);
		SearchableComboBox txt08 = createComboBox ("paises");imagePanel.add (txt08);txt08.setBounds (204, 195, 280, 18);
		SearchableComboBox txt09 = createComboBox ("derivado_aduanas", txt08);imagePanel.add (txt09);txt09.setBounds (687, 195, 280, 18);
		SearchableComboBox txt10 = createComboBox ("paises");imagePanel.add (txt10);txt10.setBounds (204, 218, 280, 18);
		SearchableComboBox txt11 = createComboBox ("derivado_aduanas", txt10);imagePanel.add (txt11);txt11.setBounds (687, 218, 280, 18);
		//JTextField txt12 = new JTextField ();imagePanel.add (txt12);txt12.setBounds (204, 241, 740, 18);
		//JTextField txt13 = new JTextField ();imagePanel.add (txt13);txt13.setBounds (204, 620, 280, 18);
		//JTextField txt14 = new JTextField ();imagePanel.add (txt14);txt14.setBounds (687, 620, 280, 18);
		//JTextField txt15 = new JTextField ();imagePanel.add (txt15);txt15.setBounds (204, 643, 260, 18);
		//JTextField txt16 = new JTextField ();imagePanel.add (txt16);txt16.setBounds (687, 643, 280, 18);

		return imagePanel;
	}


	

}
