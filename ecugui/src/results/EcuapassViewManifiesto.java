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

public class EcuapassViewManifiesto extends EcuapassView {
	public EcuapassViewManifiesto () {
		super ();
		resourcesDir = "/data_ecuapass/";
		//URL imgPath = getClass ().getClassLoader ().getResource ("resources/images/image-manifiesto-ecuapass.png");
		URL imgPath = getClass().getResource("/resources/images/image-manifiesto-ecuapass.png");
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

			EcuapassViewManifiesto sp = new EcuapassViewManifiesto ();

			frame.getContentPane ().add (sp, BorderLayout.CENTER);
			frame.setPreferredSize (new Dimension (1000, 600));
			frame.pack ();
			frame.setVisible (true);
		});
	}


	public ArrayList <Component> getInputTextFields () {
		ArrayList <Component> imagePanel = new ArrayList <> ();
		SearchableComboBox txt01 = createComboBox ("procedimientos");imagePanel.add (txt01);txt01.setBounds (202, 126, 280, 20);
		SearchableComboBox txt02 = createComboBox ("sectores");imagePanel.add (txt02);txt02.setBounds (684, 126, 280, 20);
		JTextField txt03 = new JTextField ();imagePanel.add (txt03);txt03.setBounds (202, 149, 78, 20);
		SearchableComboBox txt04 = createComboBox ("distritos");imagePanel.add (txt04);txt04.setBounds (684, 149, 280, 20);
		JTextField txt05 = new JTextField ();imagePanel.add (txt05);txt05.setBounds (202, 172, 280, 20);
		SearchableComboBox txt06 = createComboBox ("empresas_transporte");imagePanel.add (txt06);txt06.setBounds (684, 172, 280, 20);
		txt06.setEnabled (false);
		JRadioButton r1 = new JRadioButton (); JRadioButton r2 = new JRadioButton (); JRadioButton r3 = new JRadioButton ();
		ButtonGroup rg = new ButtonGroup ();
		rg.add (r1); rg.add (r2); rg.add (r3);
		imagePanel.add (r1);		r1.setBounds (202, 195, 20, 20);
		imagePanel.add (r2);		r2.setBounds (343, 195, 20, 20);
		imagePanel.add (r3);		r3.setBounds (500, 195, 20, 20);
		JTextField txt10 = new JTextField ();imagePanel.add (txt10);txt10.setBounds (202, 218, 280, 20);
		JTextField txt11 = new JTextField ();imagePanel.add (txt11);txt11.setBounds (684, 218, 280, 20);
		JTextField txt12 = new JTextField ();imagePanel.add (txt12);txt12.setBounds (202, 241, 280, 20);
		JTextField txt13 = new JTextField ();imagePanel.add (txt13);txt13.setBounds (684, 241, 280, 20);
		JTextField txt14 = new JTextField ();imagePanel.add (txt14);txt14.setBounds (202, 264, 280, 20);
		JTextField txt15 = new JTextField ();imagePanel.add (txt15);txt15.setBounds (684, 264, 280, 20);
		JTextField txt16 = new JTextField ();imagePanel.add (txt16);txt16.setBounds (202, 287, 280, 20);
		JTextField txt17 = new JTextField ();imagePanel.add (txt17);txt17.setBounds (202, 333, 280, 20);
		JTextField txt18 = new JTextField ();imagePanel.add (txt18);txt18.setBounds (684, 333, 280, 20);
		SearchableComboBox txt19 = createComboBox ("paises");imagePanel.add (txt19);txt19.setBounds (202, 356, 280, 20);
		JTextField txt20 = new JTextField ();imagePanel.add (txt20);txt20.setBounds (684, 356, 280, 20);
		JTextField txt21 = new JTextField ();imagePanel.add (txt21);txt21.setBounds (202, 379, 280, 20);
		JTextField txt22 = new JTextField ();imagePanel.add (txt22);txt22.setBounds (684, 379, 280, 20);
		SearchableComboBox txt23 = createComboBox ("tipos_vehiculo");imagePanel.add (txt23);txt23.setBounds (202, 402, 280, 20);
		JTextField txt24 = new JTextField ();imagePanel.add (txt24);txt24.setBounds (202, 448, 280, 20);
		JTextField txt25 = new JTextField ();imagePanel.add (txt25);txt25.setBounds (684, 448, 280, 20);
		JTextField txt26 = new JTextField ();imagePanel.add (txt26);txt26.setBounds (202, 471, 280, 20);
		SearchableComboBox txt27 = createComboBox ("paises");imagePanel.add (txt27);txt27.setBounds (684, 471, 280, 20);
		JTextField txt28 = new JTextField ();imagePanel.add (txt28);txt28.setBounds (202, 494, 280, 20);
		JTextField txt29 = new JTextField ();imagePanel.add (txt29);txt29.setBounds (684, 494, 280, 20);
		SearchableComboBox txt30 = createComboBox ("paises");imagePanel.add (txt30);txt30.setBounds (202, 540, 280, 20);
		SearchableComboBox txt31 = createComboBox ("tipos_documento");imagePanel.add (txt31);txt31.setBounds (684, 540, 280, 20);
		JTextField txt32 = new JTextField ();imagePanel.add (txt32);txt32.setBounds (202, 563, 280, 20);
		SearchableComboBox txt33 = createComboBox ("tipos_sexo");imagePanel.add (txt33);txt33.setBounds (586, 563, 95, 20);
		JTextField txt34 = new JTextField ();imagePanel.add (txt34);txt34.setBounds (862, 563, 78, 20);
		JTextField txt35 = new JTextField ();imagePanel.add (txt35);txt35.setBounds (202, 586, 762, 20);
		JTextField txt36 = new JTextField ();imagePanel.add (txt36);txt36.setBounds (202, 609, 280, 20);
		JTextField txt37 = new JTextField ();imagePanel.add (txt37);txt37.setBounds (684, 609, 280, 20);
		SearchableComboBox txt38 = createComboBox ("paises");imagePanel.add (txt38);txt38.setBounds (202, 632, 280, 20);
		SearchableComboBox txt39 = createComboBox ("tipos_documento");imagePanel.add (txt39);txt39.setBounds (684, 632, 280, 20);
		JTextField txt40 = new JTextField ();imagePanel.add (txt40);txt40.setBounds (202, 655, 280, 20);
		SearchableComboBox txt41 = createComboBox ("tipos_sexo");imagePanel.add (txt41);txt41.setBounds (586, 655, 95, 20);
		JTextField txt42 = new JTextField ();imagePanel.add (txt42);txt42.setBounds (862, 655, 78, 20);
		JTextField txt43 = new JTextField ();imagePanel.add (txt43);txt43.setBounds (202, 678, 280, 20);
		JTextField txt44 = new JTextField ();imagePanel.add (txt44);txt44.setBounds (684, 678, 280, 20);
		JTextField txt45 = new JTextField ();imagePanel.add (txt45);txt45.setBounds (202, 701, 280, 20);
		JTextField txt46 = new JTextField ();imagePanel.add (txt46);txt46.setBounds (684, 701, 280, 20);
		SearchableComboBox txt47 = createComboBox ("paises");imagePanel.add (txt47);txt47.setBounds (202, 747, 137, 20);
		SearchableComboBox txt48 = createComboBox ("derivado_ciudades", txt47);imagePanel.add (txt48);txt48.setBounds (345, 747, 137, 20);
		SearchableComboBox txt49 = createComboBox ("paises");imagePanel.add (txt49);txt49.setBounds (684, 747, 137, 20);
		SearchableComboBox txt50 = createComboBox ("derivado_ciudades", txt49);imagePanel.add (txt50);txt50.setBounds (826, 747, 137, 20);
		SearchableComboBox txt51 = createComboBox ("tipos_carga");imagePanel.add (txt51);txt51.setBounds (202, 770, 280, 20);
		JScrollPane txt52 = new JScrollPane (new JTextArea (2,40));imagePanel.add (txt52);txt52.setBounds (202, 793, 762, 66);
		JTextField txt53 = new JTextField ();imagePanel.add (txt53);txt53.setBounds (202, 861, 280, 20);
		SearchableComboBox txt54 = createComboBox ("tipos_incoterm");imagePanel.add (txt54);txt54.setBounds (684, 861, 280, 20);
		SearchableComboBox txt55 = createComboBox ("monedas");imagePanel.add (txt55);txt55.setBounds (202, 884, 280, 20);
		SearchableComboBox txt56 = createComboBox ("paises");imagePanel.add (txt56);txt56.setBounds (684, 884, 137, 20);
		SearchableComboBox txt57 = createComboBox ("derivado_ciudades", txt56);imagePanel.add (txt57);txt57.setBounds (826, 884, 137, 20);
		SearchableComboBox txt58 = createComboBox ("paises");imagePanel.add (txt58);txt58.setBounds (202, 907, 280, 20);
		SearchableComboBox txt59 = createComboBox ("derivado_aduanas", txt58);imagePanel.add (txt59);txt59.setBounds (684, 907, 280, 20);
		JTextField txt60 = new JTextField ();imagePanel.add (txt60);txt60.setBounds (202, 930, 280, 20);
		JTextField txt61 = new JTextField ();imagePanel.add (txt61);txt61.setBounds (684, 930, 280, 20);
		JTextField txt62 = new JTextField ();imagePanel.add (txt62);txt62.setBounds (202, 953, 280, 20);
		JTextField txt63 = new JTextField ();imagePanel.add (txt63);txt63.setBounds (684, 953, 280, 20);
		SearchableComboBox txt64 = createComboBox ("paises");imagePanel.add (txt64);txt64.setBounds (202, 1175, 280, 20);
		SearchableComboBox txt65 = createComboBox ("derivado_aduanas", txt64);imagePanel.add (txt65);txt65.setBounds (684, 1175, 280, 20);
		JTextField txt66 = new JTextField ();imagePanel.add (txt66);txt66.setBounds (202, 1523, 280, 20);
		JTextField txt67 = new JTextField ();imagePanel.add (txt67);txt67.setBounds (684, 1523, 280, 20);
		JTextField txt68 = new JTextField ();imagePanel.add (txt68);txt68.setBounds (202, 1546, 280, 20);
		JTextField txt69 = new JTextField ();imagePanel.add (txt69);txt69.setBounds (684, 1546, 251, 20);
		JTextField txt70 = new JTextField ();imagePanel.add (txt70);txt70.setBounds (202, 1569, 280, 20);
		SearchableComboBox txt71 = createComboBox ("tipos_embalaje");imagePanel.add (txt71);txt71.setBounds (684, 1569, 280, 20);
		JTextField txt72 = new JTextField ();imagePanel.add (txt72);txt72.setBounds (202, 1592, 280, 20);
		JTextField txt73 = new JTextField ();imagePanel.add (txt73);txt73.setBounds (684, 1592, 280, 20);
		JTextField txt74 = new JTextField ();imagePanel.add (txt74);txt74.setBounds (202, 1615, 280, 20);
		JTextField txt75 = new JTextField ();imagePanel.add (txt75);txt75.setBounds (684, 1615, 280, 20);
		JTextField txt76 = new JTextField ();imagePanel.add (txt76);txt76.setBounds (202, 1638, 280, 20);
		JTextField txt77 = new JTextField ();imagePanel.add (txt77);txt77.setBounds (684, 1638, 280, 20);
		SearchableComboBox txt78 = createComboBox ("tipos_unidadcarga");imagePanel.add (txt78);txt78.setBounds (202, 1661, 280, 20);
		SearchableComboBox txt79 = createComboBox ("condiciones_unidadcarga");imagePanel.add (txt79);txt79.setBounds (684, 1661, 280, 20);
		JTextField txt80 = new JTextField ();imagePanel.add (txt80);txt80.setBounds (202, 1684, 280, 20);
		JScrollPane txt81 = new JScrollPane (new JTextArea (2,40));imagePanel.add (txt81);txt81.setBounds (202, 1707, 762, 66);
		JTextField txt82 = new JTextField ();imagePanel.add (txt82);txt82.setBounds (202, 2075, 762, 20);

		return imagePanel;
	}
	

}
