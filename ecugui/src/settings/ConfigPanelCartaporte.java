package settings;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;

/*
 * Panel for set config parameters to take into account when
 * extracting EcuapassFields from DocumentFields
 */

public class ConfigPanelCartaporte extends ConfigPanel {
    @Override
    public void addAllFields() {
        JButton button02 = createButton("02_Remitente");       JTextField text02 = createTextField("");   addRow(button02, text02);
        JButton button03 = createButton("03_Destinatario");    JTextField text03 = createTextField("");   addRow(button03, text03);
        JButton button04 = createButton("04_Consignatario");   JTextField text04 = createTextField("");   addRow(button04, text04);
        JButton button05 = createButton("05_Notificado");      JTextField text05 = createTextField("");   addRow(button05, text05);
        JButton button08 = createButton("08_Entrega");         JTextField text08 = createTextField("");   addRow(button08, text08);
        JButton button09 = createButton("09_Condiciones");     JTextField text09 = createTextField("");   addRow(button09, text09);
        JButton button10 = createButton("10_CantidadClase_Bultos"); JTextField text10 = createTextField(""); addRow(button10, text10);
        JButton button11 = createButton("11_MarcasNumeros_Bultos"); JTextField text11 = createTextField(""); addRow(button11, text11);
        JButton button12 = createButton("12_Descripcion_Bultos");   JTextField text12 = createTextField(""); addRow(button12, text12);
        JButton button18 = createButton("18_Documentos");      JTextField text18 = createTextField("");   addRow(button18, text18);
        JButton button21 = createButton("21_Instrucciones");   JTextField text21 = createTextField("");   addRow(button21, text21);
        JButton button22 = createButton("22_Observaciones");   JTextField text22 = createTextField("");   addRow(button22, text22);
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Scrollable Panel");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);

        ConfigPanelCartaporte scrollPanel = new ConfigPanelCartaporte();
        frame.setContentPane(scrollPanel);
        frame.setVisible(true);
    }
}
