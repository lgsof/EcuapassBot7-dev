package widgets;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class ColorButton extends JButton {

    private static Color normalColor = new Color(241, 241, 0);
    private static Color hoverColor = new Color(230, 230, 0);
    private static Color pressColor = new Color(220, 220, 0);
    private static Color textColor = Color.BLACK;

    public ColorButton() {
        this("", normalColor, hoverColor, pressColor, textColor);
    }

    public ColorButton(String text) {
        this(text, normalColor, hoverColor, pressColor, textColor);
    }

    public ColorButton(String text, Color normalColor, Color hoverColor, Color pressColor, Color textColor) {
        super(text);
        // Set initial appearance
        setBackground(normalColor);
        setForeground(textColor);
        setContentAreaFilled(false);
        setOpaque(true);
        setBorderPainted(true);
        setFocusPainted(false);
        setFont(new Font("Segoe UI", Font.PLAIN, 14));
        setBorder(BorderFactory.createEmptyBorder(8, 15, 8, 15));

        // Add hover and press effects
        addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                setBackground(hoverColor);
            }

            public void mouseExited(java.awt.event.MouseEvent evt) {
                setBackground(normalColor);
            }

            public void mousePressed(java.awt.event.MouseEvent evt) {
                setBackground(pressColor);
            }

            public void mouseReleased(java.awt.event.MouseEvent evt) {
                setBackground(normalColor);
            }
        });
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = (Graphics2D) g.create();

        // Set background based on state
        if (!isEnabled()) {
            g2.setColor(new Color(200, 200, 200)); // Disabled bg
        } else if (getModel().isPressed()) {
            g2.setColor(pressColor);
        } else if (getModel().isRollover()) {
            g2.setColor(hoverColor);
        } else {
            g2.setColor(normalColor);
        }

        // Paint background
        g2.fillRect(0, 0, getWidth(), getHeight());

        // Paint text manually
        FontMetrics fm = g2.getFontMetrics();
        String text = getText();
        int textWidth = fm.stringWidth(text);
        int textHeight = fm.getAscent();

        int x = (getWidth() - textWidth) / 2;
        int y = (getHeight() + textHeight) / 2 - 2;

        if (!isEnabled()) {
            g2.setColor(new Color(100, 100, 100)); // Disabled text
        } else {
            g2.setColor(textColor);
        }

        g2.drawString(text, x, y);
        g2.dispose();
    }

//	protected void paintComponent (Graphics g) {
//		// Paint background
//		Graphics2D g2 = (Graphics2D) g.create ();
//		g2.setRenderingHint (RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
//		g2.setColor (getBackground ());
//		g2.fillRoundRect (0, 0, getWidth (), getHeight (), 8, 8);
//		g2.dispose ();
//
//		super.paintComponent (g);
//	}
    // Test Main
    public static void main(String[] args) {
        // Set system look and feel
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Create frame
        JFrame frame = new JFrame("ColorButton Demo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 300);
        frame.setLayout(new FlowLayout(FlowLayout.CENTER, 15, 15));

        // Create buttons with different colors
        ColorButton primaryBtn = new ColorButton(
                "Primary",
                new Color(241, 241, 0),
                new Color(220, 220, 0),
                new Color(200, 200, 0),
                Color.BLACK
        );

        ColorButton successBtn = new ColorButton(
                "Success",
                new Color(40, 180, 100),
                new Color(35, 160, 85),
                new Color(30, 140, 70),
                Color.WHITE
        );

        ColorButton dangerBtn = new ColorButton(
                "Danger",
                new Color(220, 60, 60),
                new Color(200, 50, 50),
                new Color(180, 40, 40),
                Color.WHITE
        );

        ColorButton warningBtn = new ColorButton("Test");

        // Add action listeners
        ActionListener listener = e -> {
            JButton source = (JButton) e.getSource();
            JOptionPane.showMessageDialog(frame, "Clicked: " + source.getText());
        };

        primaryBtn.addActionListener(listener);
        successBtn.addActionListener(listener);
        dangerBtn.addActionListener(listener);
        warningBtn.addActionListener(listener);

        // Add buttons to frame
        frame.add(primaryBtn);
        frame.add(successBtn);
        frame.add(dangerBtn);
        frame.add(warningBtn);

        // Show frame
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }
}
