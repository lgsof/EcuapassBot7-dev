package settings;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;

/*
 * Panel for set config parameters to take into account when
 * extracting EcuapassFields from DocumentFields
 */

public class ConfigPanelManifiesto extends ConfigPanel {
    @Override
    public void addAllFields() {
        addRow (createButton("29_Mercancia_Descripcion"), createTextField(""));
        JButton button30 = createButton("30_Mercancia_Bultos");  JTextField text30 = createTextField("");   addRow(button30, text30);
        JButton button31 = createButton("31_Mercancia_Embalaje");  JTextField text31 = createTextField("");   addRow(button31, text31);
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Scrollable Panel");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);

        ConfigPanelManifiesto scrollPanel = new ConfigPanelManifiesto();
        frame.setContentPane(scrollPanel);
        frame.setVisible(true);
    }
}
