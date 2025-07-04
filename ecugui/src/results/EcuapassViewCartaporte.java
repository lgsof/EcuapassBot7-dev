package results;

import documento.DocModel;
import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import java.net.URL;
import java.util.ArrayList;
import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import widgets.SearchableComboBox;

public class EcuapassViewCartaporte extends EcuapassView {
	public EcuapassViewCartaporte () {
		super ();
		resourcesDir = "/data_ecuapass/";
		URL imgPath = getClass ().getClassLoader ().getResource ("resources/images/image-cartaporte-ecuapass.png");
		//URL imgPath = new URL ("/home/lg/BIO/iaprojects/ecuapass/cartaportes/ecugui/resources/images/image-cartaporte-ecuapass.png");
		ecuapassPanel = new EcuapassPanel (imgPath);
		Dimension size = new Dimension (960, 1410);
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

			EcuapassViewCartaporte sp = new EcuapassViewCartaporte ();

			frame.getContentPane ().add (sp, BorderLayout.CENTER);
			frame.setPreferredSize (new Dimension (800, 600));
			frame.pack ();
			frame.setVisible (true);
		});
	}
	

	public ArrayList <Component> getInputTextFields () {
		ArrayList <Component> imagePanel = new ArrayList <> ();
		SearchableComboBox txt01 = createComboBox ("distritos");imagePanel.add (txt01);txt01.setBounds (202, 31, 280, 20);
		JTextField txt02 = new JTextField ();imagePanel.add (txt02);txt02.setBounds (684, 31, 280, 20);
		JTextField txt03 = new JTextField ();imagePanel.add (txt03);txt03.setBounds (202, 54, 280, 20);
		JTextField txt04 = new JTextField ();imagePanel.add (txt04);txt04.setBounds (684, 54, 280, 20);
		SearchableComboBox txt05 = createComboBox ("procedimientos");imagePanel.add (txt05);txt05.setBounds (202, 77, 280, 20);
		JTextField txt06 = new JTextField ();imagePanel.add (txt06);txt06.setBounds (684, 77, 280, 20);
		SearchableComboBox txt07 = createComboBox ("derivado_depositos", txt01);imagePanel.add (txt07);txt07.setBounds (202, 100, 280, 20);
		JTextField txt08 = new JTextField ();imagePanel.add (txt08);txt08.setBounds (684, 100, 280, 20);
		JTextField txt09 = new JTextField ();imagePanel.add (txt09);txt09.setBounds (202, 123, 280, 20);
		SearchableComboBox txt10 = createComboBox ("paises");imagePanel.add (txt10);txt10.setBounds (202, 169, 280, 20);
		JTextField txt11 = new JTextField ();imagePanel.add (txt11);txt11.setBounds (684, 169, 280, 20);
		JTextField txt12 = new JTextField ();imagePanel.add (txt12);txt12.setBounds (202, 192, 280, 20);
		JTextField txt13 = new JTextField ();imagePanel.add (txt13);txt13.setBounds (684, 192, 280, 20);
		JTextField txt14 = new JTextField ();imagePanel.add (txt14);txt14.setBounds (202, 215, 762, 20);
		JTextField txt15 = new JTextField ();imagePanel.add (txt15);txt15.setBounds (202, 238, 762, 20);
		SearchableComboBox txt16 = createComboBox ("paises");imagePanel.add (txt16);txt16.setBounds (202, 261, 280, 20);
		JTextField txt17 = new JTextField ();imagePanel.add (txt17);txt17.setBounds (684, 261, 280, 20);
		JTextField txt18 = new JTextField ();imagePanel.add (txt18);txt18.setBounds (202, 284, 280, 20);
		JTextField txt19 = new JTextField ();imagePanel.add (txt19);txt19.setBounds (202, 307, 762, 20);
		JTextField txt20 = new JTextField ();imagePanel.add (txt20);txt20.setBounds (202, 330, 762, 20);
		SearchableComboBox txt21 = createComboBox ("paises");imagePanel.add (txt21);txt21.setBounds (202, 353, 280, 20);
		JTextField txt22 = new JTextField ();imagePanel.add (txt22);txt22.setBounds (684, 353, 280, 20);
		JTextField txt23 = new JTextField ();imagePanel.add (txt23);txt23.setBounds (202, 376, 280, 20);
		JTextField txt24 = new JTextField ();imagePanel.add (txt24);txt24.setBounds (202, 399, 762, 20);
		JTextField txt25 = new JTextField ();imagePanel.add (txt25);txt25.setBounds (202, 422, 762, 20);
		JTextField txt26 = new JTextField ();imagePanel.add (txt26);txt26.setBounds (202, 445, 762, 20);
		JTextField txt27 = new JTextField ();imagePanel.add (txt27);txt27.setBounds (202, 468, 762, 20);
		// Pais del notificado
		SearchableComboBox txt28 = createComboBox ("paises");imagePanel.add (txt28);txt28.setBounds (202, 491, 280, 20);
		SearchableComboBox txt29 = createComboBox ("paises");imagePanel.add (txt29);txt29.setBounds (202, 514, 138, 20);
		SearchableComboBox txt30 = createComboBox ("derivado_ciudades", txt29);imagePanel.add (txt30);txt30.setBounds (342, 514, 138, 20);
		JTextField txt31 = new JTextField ();imagePanel.add (txt31);txt31.setBounds (684, 514, 82, 20);
		SearchableComboBox txt32 = createComboBox ("paises");imagePanel.add (txt32);txt32.setBounds (202, 537, 138, 20);
		SearchableComboBox txt33 = createComboBox ("derivado_ciudades", txt32);imagePanel.add (txt33);txt33.setBounds (342, 537, 138, 20);
		JTextField txt34 = new JTextField ();imagePanel.add (txt34);txt34.setBounds (684, 537, 82, 20);
		SearchableComboBox txt35 = createComboBox ("paises");imagePanel.add (txt35);txt35.setBounds (202, 560, 138, 20);
		SearchableComboBox txt36 = createComboBox ("derivado_ciudades", txt35);imagePanel.add (txt36);txt36.setBounds (342, 560, 138, 20);
		JTextField txt37 = new JTextField ();imagePanel.add (txt37);txt37.setBounds (684, 560, 82, 20);
		SearchableComboBox txt38 = createComboBox ("condiciones_transporte");imagePanel.add (txt38);txt38.setBounds (202, 583, 280, 20);
		SearchableComboBox txt39 = createComboBox ("condiciones_pago");imagePanel.add (txt39);txt39.setBounds (684, 583, 280, 20);
		JTextField txt40 = new JTextField ();imagePanel.add (txt40);txt40.setBounds (202, 606, 280, 20);
		JTextField txt41 = new JTextField ();imagePanel.add (txt41);txt41.setBounds (684, 606, 280, 20);
		JTextField txt42 = new JTextField ();imagePanel.add (txt42);txt42.setBounds (202, 629, 280, 20);
		JTextField txt43 = new JTextField ();imagePanel.add (txt43);txt43.setBounds (684, 629, 280, 20);
		JTextField txt44 = new JTextField ();imagePanel.add (txt44);txt44.setBounds (202, 652, 280, 20);
		JTextField txt45 = new JTextField ();imagePanel.add (txt45);txt45.setBounds (684, 652, 280, 20);
		JTextField txt46 = new JTextField ();imagePanel.add (txt46);txt46.setBounds (202, 675, 280, 20);
		JTextField txt47 = new JTextField ();imagePanel.add (txt47);txt47.setBounds (684, 675, 280, 20);
		SearchableComboBox txt48 = createComboBox ("paises");imagePanel.add (txt48);txt48.setBounds (202, 698, 138, 20);
		SearchableComboBox txt49 = createComboBox ("derivado_ciudades", txt48);imagePanel.add (txt49);txt49.setBounds (342, 698, 138, 20);
		JTextField txt50 = new JTextField ();imagePanel.add (txt50);txt50.setBounds (202, 721, 280, 20);
		JTextField txt51 = new JTextField ();imagePanel.add (txt51);txt51.setBounds (684, 721, 280, 20);
		JTextField txt52 = new JTextField ();imagePanel.add (txt52);txt52.setBounds (202, 744, 280, 20);
		JTextField txt53 = new JTextField ();imagePanel.add (txt53);txt53.setBounds (684, 744, 280, 20);
		JTextField txt54 = new JTextField ();imagePanel.add (txt54);txt54.setBounds (202, 767, 280, 20);
		JTextField txt55 = new JTextField ();imagePanel.add (txt55);txt55.setBounds (684, 767, 280, 20);
		JTextField txt56 = new JTextField ();imagePanel.add (txt56);txt56.setBounds (202, 790, 280, 20);
		JTextField txt57 = new JTextField ();imagePanel.add (txt57);txt57.setBounds (684, 790, 280, 20);
		JTextField txt58 = new JTextField ();imagePanel.add (txt58);txt58.setBounds (202, 813, 280, 20);
		JTextField txt59 = new JTextField ();imagePanel.add (txt59);txt59.setBounds (684, 813, 280, 20);
		JTextField txt60 = new JTextField ();imagePanel.add (txt60);txt60.setBounds (202, 836, 762, 20);
		JTextField txt61 = new JTextField ();imagePanel.add (txt61);txt61.setBounds (202, 859, 82, 20);
		SearchableComboBox txt62 = createComboBox ("paises");imagePanel.add (txt62);txt62.setBounds (684, 859, 138, 20);
		SearchableComboBox txt63 = createComboBox ("derivado_ciudades", txt62);imagePanel.add (txt63);txt63.setBounds (825, 859, 138, 20);
		// Instrucciones al transportista
		JScrollPane txt64 = new JScrollPane (new JTextArea (2,40));imagePanel.add (txt64);txt64.setBounds (202, 882, 762, 46);
		JScrollPane txt65 = new JScrollPane (new JTextArea (2,40));imagePanel.add (txt65);txt65.setBounds (202, 929, 762, 46);
		JTextField txt66 = new JTextField ();imagePanel.add (txt66);txt66.setBounds (202, 999, 280, 20);
		JTextField txt67 = new JTextField ();imagePanel.add (txt67);txt67.setBounds (684, 999, 280, 20);
		SearchableComboBox txt68 = createComboBox ("tipos_embalaje");imagePanel.add (txt68);txt68.setBounds (202, 1022, 280, 20);
		JTextField txt69 = new JTextField ();imagePanel.add (txt69);txt69.setBounds (684, 1022, 280, 20);
		JTextField txt70 = new JTextField ();imagePanel.add (txt70);txt70.setBounds (202, 1045, 280, 20);
		JTextField txt71 = new JTextField ();imagePanel.add (txt71);txt71.setBounds (684, 1045, 280, 20);
		JTextField txt72 = new JTextField ();imagePanel.add (txt72);txt72.setBounds (202, 1068, 280, 20);
		JTextField txt73 = new JTextField ();imagePanel.add (txt73);txt73.setBounds (684, 1068, 280, 20);
		JTextField txt74 = new JTextField ();imagePanel.add (txt74);txt74.setBounds (202, 1091, 742, 20);
		JTextField txt75 = new JTextField ();imagePanel.add (txt75);txt75.setBounds (202, 1114, 742, 20);
		JTextField txt76 = new JTextField ();imagePanel.add (txt76);txt76.setBounds (202, 1137, 742, 20);
		JTextField txt77 = new JTextField ();imagePanel.add (txt77);txt77.setBounds (202, 1160, 742, 20);
		JTextField txt78 = new JTextField ();imagePanel.add (txt78);txt78.setBounds (202, 1183, 762, 20);
		JScrollPane txt79 = new JScrollPane (new JTextArea (10,40));imagePanel.add (txt79);txt79.setBounds (202, 1206, 762, 150);
		return imagePanel;
	}
	
}
