package main;

import documento.DocModel;
import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Desktop;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.URLConnection;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;
import javax.imageio.ImageIO;
import javax.swing.JRadioButton;
import javax.swing.JTextField;
import javax.swing.text.AbstractDocument;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.DocumentFilter;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.rendering.ImageType;
import org.apache.pdfbox.rendering.PDFRenderer;
import org.apache.pdfbox.text.PDFTextStripper;

public class Utils {

    public static Color HIGH_GREEN = new Color(240, 255, 240);
    public static Color MID_YELLOW = new Color(255, 255, 192);
    public static Color LOW_RED = new Color(255, 229, 229);
    

    // Enable/Disable all components from a container (e.g. Panel, Frame, etc)
    public static void enableComponentsPanel(Container container, boolean enableFlag) {
        container.setEnabled(enableFlag);
        Component[] components = container.getComponents();
        for (Component component : components) {
            component.setEnabled(enableFlag);
            if (component instanceof Container) {
                enableComponentsPanel((Container) component, enableFlag);
            }
        }
    }    

    // Toggle color to selected radio button
    public static void toggleRadioButtonColor(JRadioButton[] radioButtons) {
        // Loop through all radio buttons in the array
        for (JRadioButton button : radioButtons) {
            if (button.isSelected()) {
                button.setForeground(Color.BLUE);  // Set selected button color to blue
            } else {
                button.setForeground(Color.BLACK);  // Set unselected buttons color to black
            }
        }
    }

    // Get the current release from a "VERSION.txt" file
    public static String getAppRelease(String directoryPath) {
        // Create a File object for the directory
        File directory = new File(directoryPath);
        File versionFile = new File(directory, "VERSION.txt");

        // Check if the VERSION.txt file exists
        if (versionFile.exists() && versionFile.isFile())
			try (BufferedReader reader = new BufferedReader(new FileReader(versionFile))) {
            // Read the first line from the file
            String line = reader.readLine();

            if (line != null) {
                // Split the line into words
                String[] parts = line.split("\\s+");

                // Return the second string
                return parts[1];
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        // If the file doesn't exist or an error occurs, return null
        return null;
    }

    // Copy file from source to destiny checking if file exists 
    public static void copyFile(String sourceFilepath, String destFilepath) {
        //System.out.println  ("Copiando archivos:");
        try {
            File sourcePath = new File(sourceFilepath);
            File destPath = new File(destFilepath);
            //System.out.println  (">>> FUENTE: " + sourcePath);
            //System.out.println  (">>> DESTINO: " + destPath);
            if (sourcePath.getName().contains("DUMMY")) {
                destPath.createNewFile();
                return;
            }
            if (destPath.exists()) {
                Files.delete(destPath.toPath());
            }
            Files.copy(sourcePath.toPath(), destPath.toPath(), StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException ex) {
            System.out.println("No se pudo reemplazar el archivo: " + destFilepath);
            //Logger.getLogger (Utils.class.getName ()).log (Level.SEVERE, null, ex);
        }

    }

    // Extract the last country from a text
    public static String extractLastCountry(String text, String[] countries) {
        String lastCountry = null;
        int lastIndex = -1;

        for (String country : countries) {
            Pattern pattern = Pattern.compile("\\b" + country + "\\b", Pattern.CASE_INSENSITIVE);
            Matcher matcher = pattern.matcher(text);

            while (matcher.find()) {
                if (matcher.end() > lastIndex) {
                    lastIndex = matcher.end();
                    lastCountry = country;
                }
            }
        }
        return lastCountry;
    }

    // Extract the document number from a filename
    public static String extractDocNumber(String filename) {
        String docNumber = null;
        try {
            if ("ALDIA".equals(DocModel.empresa)) {
                Pattern pattern = Pattern.compile("\\d{4,}");
                Matcher matcher = pattern.matcher(filename);
                if (matcher.find()) {
                    docNumber = matcher.group();
                }
            } else {
                Pattern pattern = Pattern.compile("(?:^|[^A-Z])(CO|COCO|EC|ECEC|PE|PEPE)(\\d+)");
                Matcher matcher = pattern.matcher(filename);
                if (matcher.find()) {
                    String prefix = matcher.group(1);
                    prefix = prefix.replace("COCO", "CO");
                    prefix = prefix.replace("ECEC", "EC");
                    prefix = prefix.replace("PEPE", "PE");

                    docNumber = prefix + matcher.group(2); // Combine prefix and number
                }
            }
            return docNumber;
        } catch (Exception e) {
            e.printStackTrace();
            return null; // No match found
        }
    }

    // Return document type if document title is found in PDF lines
    public static String getDocumentTypeFromPDF(String pdfFilepath) {
        String textDeclaracion = "Declaración de Tránsito Aduanero Internacional ";
        String textManifiesto = "Manifiesto de Carga Internacional";
        String textCartaporte = "Carta de Porte Internacional por Carretera";

        String[] lines = getLinesFromPDF(pdfFilepath);
        for (String line : lines) {
            if (line.contains(textCartaporte)) {
                return "CARTAPORTE";
            } else if (line.contains(textManifiesto)) {
                return "MANIFIESTO";
            } else if (line.contains(textDeclaracion)) {
                return "DECLARACION";
            }
        }
        return null;
    }

    public static String getDocumentTypeFromFilename(String filename) {
        filename = filename.toUpperCase();
        if (filename.contains("CPI") || filename.contains("CARTAPORTE")) {
            return "CARTAPORTE";
        } else if (filename.contains("MCI") || filename.contains("MANIFIESTO")) {
            return "MANIFIESTO";
        } else {
            return null;
        }
    }

    public static String getDocTypeShortname(String docType) {
        switch (docType) {
            case "CARTAPORTE":
                return "CPI";
            case "MANIFIESTO":
                return "MCI";
            default:
                return "NONE";
        }
    }
    // Create filename from view doc number and doc type

    public static String createDummyFile(String docNumber, String docType) {
        String docTypeShortname = Utils.getDocTypeShortname(docType);
        String dummyFilename = "DUMMY-" + docTypeShortname + "-" + docNumber + ".pdf";
        return dummyFilename;
    }

    public static String[] getLinesFromPDF(String pdfFilepath) {
        String[] lines = null;
        try {
            File pdfFile = new File(pdfFilepath); // Replace with the path to your PDF file
            PDDocument document = PDDocument.load(pdfFile);

            PDFTextStripper pdfTextStripper = new PDFTextStripper();
            String pdfText = pdfTextStripper.getText(document);

            lines = pdfText.split("\\r?\\n"); // Split the text into lines
            document.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return lines;
    }

    // Convert first page PDF file to image and write to tmpDir
    public static File convertPDFToImage(File pdfFilepath) {
        File tmpDir = new File(System.getProperty("java.io.tmpdir"));
        File outImgFilepath = new File(tmpDir, pdfFilepath.getName().replace(".pdf", ".jpg"));
        if (outImgFilepath.exists()) {
            return (outImgFilepath);
        }
        //else:
        try {
            PDDocument document = PDDocument.load(pdfFilepath);
            PDFRenderer pdfRenderer = new PDFRenderer(document);

            int numberOfPages = document.getNumberOfPages();

            int dpi = 200;// use less dpi for to save more space in harddisk. For professional usage you can use more than 300dpi 
            BufferedImage bImage = pdfRenderer.renderImageWithDPI(0, dpi, ImageType.RGB);
            ImageIO.write(bImage, "jpg", outImgFilepath);
            document.close();

        } catch (IOException ex) {
            Logger.getLogger(Utils.class
                    .getName()).log(Level.SEVERE, null, ex);
        }
        return (outImgFilepath);
    }

    // Return if a file is a pdf or a image or none
    public static String getFileContentType(File file) {
        String mimeType = URLConnection.guessContentTypeFromName(file.getName());
        if (mimeType.contains("pdf")) {
            return ("pdf");
        } else if (mimeType.contains("image")) {
            return ("image");
        } else {
            return ("");
        }
    }

    // Get OS name
    public static String getOSName() {
        String OSType = System.getProperty("os.name").toLowerCase();
        if (OSType.contains("windows")) {
            return ("windows");
        } else {
            return ("linux");
        }
    }

    // Return OS tmp dir
    public static File getOSTmpDir() {
        File tmpDir = new File(System.getProperty("java.io.tmpdir"));
        return (tmpDir);
    }

    // Return save/open projects directory 
    public static String convertToOSPath(String path) {
        if (getOSName().equals("windows")) {
            path = path.replace("\\", "\\\\");
        }
        return (path);
    }

    public static String getResultsFile(String docFilepath, String sufixString) {
        String fileName = new File(docFilepath).getPath();
        String docFilename = fileName.substring(0, fileName.lastIndexOf('.'));
        String resultsFilename = String.format("%s-%s", docFilename, sufixString);
        File resultsFilepath = new File(resultsFilename);
        return (resultsFilepath.toString());
    }

    public static String getResourcePath(Object obj, String resourceName) {
        URL resourceURL = null;
        resourceURL = obj.getClass().getClassLoader().getResource("resources/" + resourceName);
        return (resourceURL.getPath());
    }

    public static String getResourcePathFromTmpDir(String resourceName) {
        String resourcesFile = Paths.get(DocModel.temporalPath, "resources", resourceName).toString();
        return (resourcesFile);

    }

//	public static String getResourcePath (String runningPath, String resourceName) {
//		Path resourcePath = Paths.get (runningPath, resourceName);
//		return (resourcePath.toString ());
//	}
    public static String createTempCompressedFileFromText(String text) {
        File tempFile = null;
        try {
            // Create a temporary file to hold the compressed data
            tempFile = File.createTempFile("compressed", ".zip");

            // Create a ZipOutputStream to write to the temporary file
            try (FileOutputStream fos = new FileOutputStream(tempFile); ZipOutputStream zipOut = new ZipOutputStream(fos)) {
                // Add a new ZIP entry
                zipOut.putNextEntry(new ZipEntry("text.txt"));

                // Write the text content to the ZIP entry
                zipOut.write(text.getBytes());

                // Close the ZIP entry
                zipOut.closeEntry();

            }
        } catch (IOException ex) {
            Logger.getLogger(Utils.class
                    .getName()).log(Level.SEVERE, null, ex);
        }

        return Utils.convertToOSPath(tempFile.toString());
    }

    // Used to read and fill Ecuapass comboBoxes (e.g paises, ciudades, etc.)
    public static String[] readDataFromFile(String filename) {
        List<String> data = new ArrayList<>();
        String[] arrData = null;
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = (String) reader.readLine()) != null) {
                if (line.contains("+++")) {
                    continue;
                }
                data.add(new String(line.getBytes(), "UTF-8"));
            }
            arrData = data.toArray(new String[0]);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return arrData;
    }

    // Used to read to fill Ecuapass comboBoxes (e.g paises, ciudades, etc.)
    public static String[] readDataResourceFromFile(Object obj, String filename) {
        String resourcesPath = Utils.getResourcePath(obj, "");
        filename = resourcesPath + filename;
        List<String> data = new ArrayList<>();
        String[] arrData = null;
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = (String) reader.readLine()) != null) {
                data.add(new String(line.getBytes(), "UTF-8"));
            }
            arrData = data.toArray(new String[0]);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return arrData;
    }

    public static void openPdfFile(String pdfFilepath) {
        try {
            // Specify the path to the PDF file you want to open
            File pdfFile = new File(pdfFilepath);

            if (Desktop.isDesktopSupported()) {
                Desktop desktop = Desktop.getDesktop();

                if (pdfFile.exists() && pdfFile.getName().toLowerCase().endsWith(".pdf")) {
                    desktop.open(pdfFile);
                } else {
                    System.out.println(">>> The specified file is not a valid PDF.");
                }
            } else {
                System.out.println(">>> Desktop API is not supported on this platform.");
            }
        } catch (Exception e) {
            System.out.println("+++ Excepción abriendo archivo PDF: " + e.toString());
        }
    }

    public static void main(String[] args) {
        Utils.convertPDFToImage(new File("/home/lg/AAA/factura-oxxo2.pdf"));
    }

    // A default image is returned according to the document type
    public static File getDefaultDocImage(File docFilepath, Object obj) {
        try {
            String docType = Utils.getDocumentTypeFromFilename(docFilepath.getName());
            String imagePath = null;
            if (docType.equals("CARTAPORTE")) {
                imagePath = Utils.getResourcePathFromTmpDir("images/cartaporte-DUMMY.png");
            } else if (docType.equals("MANIFIESTO")) {
                imagePath = Utils.getResourcePathFromTmpDir("images/manifiesto-DUMMY.png");
            } else {
                imagePath = Utils.getResourcePathFromTmpDir("images/image-DUMMY.png");
            }

            return new File(imagePath);

        } catch (Exception ex) {
            Logger.getLogger(Utils.class
                    .getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }

    public static boolean createEmptyFile(String filepath) {
        try {
            File destPath = new File(filepath);
            if (!destPath.exists()) {
                destPath.createNewFile();
                return true;
            }
        } catch (IOException ex) {
            System.out.println("No se pudo reemplazar el archivo: " + filepath);
            //Logger.getLogger (Utils.class.getName ()).log (Level.SEVERE, null, ex);
        }
        return false;
    }

    public static void applyUppercase (JTextField textField) {
        ((AbstractDocument) textField.getDocument()).setDocumentFilter(new DocumentFilter() {
            @Override
            public void insertString(DocumentFilter.FilterBypass fb, int offset, String text, AttributeSet attr) throws BadLocationException {
                super.insertString(fb, offset, filterText(text), attr);
            }

            @Override
            public void replace(DocumentFilter.FilterBypass fb, int offset, int length, String text, AttributeSet attrs) throws BadLocationException {
                super.replace(fb, offset, length, filterText(text), attrs);
            }

            private String filterText(String text) {
                return text.toUpperCase();
            }
        });
    }
    public static void applyUppercaseNoSpaces(JTextField textField) {
        ((AbstractDocument) textField.getDocument()).setDocumentFilter(new DocumentFilter() {
            @Override
            public void insertString(FilterBypass fb, int offset, String text, AttributeSet attr) throws BadLocationException {
                super.insertString(fb, offset, filterText(text), attr);
            }

            @Override
            public void replace(FilterBypass fb, int offset, int length, String text, AttributeSet attrs) throws BadLocationException {
                super.replace(fb, offset, length, filterText(text), attrs);
            }

            private String filterText(String text) {
                return text.toUpperCase().replaceAll("\\s+", "");
            }
        });
    }

}
