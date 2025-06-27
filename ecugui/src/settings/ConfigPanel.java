package settings;

import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.*;
import java.util.LinkedHashMap;
import java.util.Map;
import main.Utils;

public abstract class ConfigPanel extends JScrollPane {
    private final Color LIGHT_GREEN = new Color(200, 255, 200);
    private final Color LIGHT_RED = new Color(255, 200, 200);

    private final Map<JButton, JTextField> pairMap = new LinkedHashMap<>();

    private final JPanel contentPanel;
    private int row = 0;

    public ConfigPanel() {
        contentPanel = new JPanel(new GridBagLayout());
        setViewportView(contentPanel);
        setVerticalScrollBarPolicy(VERTICAL_SCROLLBAR_ALWAYS);
        getVerticalScrollBar().setUnitIncrement(16);

        addAllFields();
    }

   abstract public void addAllFields(); 

    JButton createButton(String text) {
        JButton b = new JButton(text);
        b.setBackground(LIGHT_GREEN);
        return b;
    }

    JTextField createTextField(String content) {
        JTextField tf = new JTextField(content, 30);
        //Utils.applyUppercase (tf);
        return tf;
    }

    void addRow(JButton button, JTextField textField) {
        GridBagConstraints gbcBtn = new GridBagConstraints();
        gbcBtn.gridx = 0;
        gbcBtn.gridy = row;
        gbcBtn.anchor = GridBagConstraints.WEST;
        gbcBtn.fill = GridBagConstraints.HORIZONTAL;
        gbcBtn.weightx = 0.3;
        gbcBtn.insets = new Insets(3, 5, 3, 5);
        contentPanel.add(button, gbcBtn);

        GridBagConstraints gbcText = new GridBagConstraints();
        gbcText.gridx = 1;
        gbcText.gridy = row++;
        gbcText.fill = GridBagConstraints.HORIZONTAL;
        gbcText.weightx = 0.7;
        //gbcText.insets = new Insets(3, 5, 3, 5);
        contentPanel.add(textField, gbcText);

        textField.getDocument().addDocumentListener(new DocumentListener() {
            public void insertUpdate(DocumentEvent e) { button.setBackground(LIGHT_RED); }
            public void removeUpdate(DocumentEvent e) { button.setBackground(LIGHT_RED); }
            public void changedUpdate(DocumentEvent e) { button.setBackground(LIGHT_RED); }
        });

        pairMap.put(button, textField);
    }

    public void resetButtonColors() {
        for (JButton b : pairMap.keySet()) {
            b.setBackground(LIGHT_GREEN);
        }
    }

    // Optional: access to text fields
    public Map<JButton, JTextField> getFieldMap() {
        return pairMap;
    }


    public LinkedHashMap<String, String> getValues () {
        LinkedHashMap<String, String> values = new LinkedHashMap<>();
        for (Map.Entry<JButton, JTextField> entry : pairMap.entrySet()) {
            String buttonText = entry.getKey().getText();
            JTextField textField = entry.getValue();

            //String id = extractIdFromButtonText(buttonText);
            String id = buttonText;
            if (id != null) {
                values.put(id, textField.getText());
            }
        }
        return values;
    }

    public void setValues(Map <String, String> values) {
        for (Map.Entry<JButton, JTextField> entry : pairMap.entrySet()) {
            JButton button = entry.getKey();
            JTextField textField = entry.getValue();

            String id = button.getText ();
            if (id != null) {
                //String key = "key" + id;
                if (values.containsKey (id)) {
                    textField.setText(values.get(id));
                    button.setBackground (LIGHT_GREEN); // optional: reset color
                }
            }
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Scrollable Panel");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);

        ConfigPanelCartaporte scrollPanel = new ConfigPanelCartaporte ();
        frame.setContentPane(scrollPanel);
        frame.setVisible(true);
    }
}
