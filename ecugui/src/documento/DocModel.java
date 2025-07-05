package documento;

import main.Controller;
import main.Utils;
import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;
import java.util.logging.Level;
import java.util.logging.Logger;

public class DocModel {
	public static String [] paises = {"COLOMBIA", "ECUADOR", "PERU", "VENEZUELA"};
	public DocRecord currentRecord = null;
	
	public static String docsPath;  // Global dir for save and open all PDF docs
	public static String runningPath;     // Application start running dir
	public static String temporalPath; // Dir for resources 
	public static String resourcesPath;
	public static String empresa; // Name of the company for selecting document cloud models
	public static String selectedFilePath;  // Current PDF file path
	
	// Piped companies with document cloud models
	public static String ecuapassdocsURL = "https://ecuapassdocs-test.up.railway.app/";
	public static String codebiniURL = "https://byza.corebd.net/";
	public static String ecuapassURL = "https://ecuapass.aduana.gob.ec/";
	public static boolean SHOW_DOCS_BUTTONS = false;
	
	// Flag files used for controlling the process
	public static String flagBotStopFilename = "flag-bot-stop.flag";  // For stopping extenal bot processing
	public static String flagServerExitFilename = "exit.txt";                   // For stopping external flask server 

	public void initGlobalPaths () {
		docsPath = this.getDocsPath ();
		temporalPath = this.getTemporalDir (docsPath);
		runningPath = Utils.convertToOSPath (System.getProperty ("user.dir"));
		resourcesPath = Paths.get (runningPath, "resources").toString();
	}

	public void printGlobalPaths (Controller controller) {
		controller.out (">>> Empresa: " + DocModel.empresa);
		controller.out (">>> Documents dir: " + docsPath);
		controller.out (">>> Temporal dir: " + temporalPath);
		controller.out (">>> Running dir: " + runningPath);
		controller.out (">>> Resources dir: " + resourcesPath);
	}

	public String getTemporalDir (String workingDir) {
		try {
			String osTempDir = Utils.convertToOSPath (System.getProperty ("java.io.tmpdir"));
			Path fullPath = Paths.get(osTempDir).toRealPath();
			//String pathName = Utils.convertToOSPath (Paths.get (workingDir).getFileName ().toString ());
			String pathName = "tmp-ecuapassdocs";
			String path = Paths.get (fullPath.toString (), pathName).toString ();
			return Utils.convertToOSPath (path);
		} catch (IOException ex) {
			Logger.getLogger (DocModel.class.getName()).log (Level.SEVERE, null, ex);
		}
		return null;
	}

	// Dir for current user sesion 
	public String getDocsPath () {
		String relativePath = Paths.get ("Documents", "Ecuapassdocs").toString ();
		Path absolutePath = Paths.get (System.getProperty ("user.home"), relativePath);
		String path = absolutePath.toString ();
		return Utils.convertToOSPath (path);
	}

	// Create dir in "Documents" for results using current time
	public String getWorkingDir (String projectsDir) {
		LocalDateTime now = LocalDateTime.now ();			// Get the current date and time
		// Define the desired date and time format with Spanish month names
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern ("dd-MMMM-yyyy-HH_mm_ss", new Locale ("es"));
		String timestamp = now.format (formatter);			// Format the current date and time to a string
		String path = Paths.get (projectsDir, timestamp).toString ();		// Create a File object representing the new folder
		return (Utils.convertToOSPath (path));
	}

	// Create folder given the absolute path
	public void createFolder (String folderName) {
		File folder = new File (folderName);
		if (folder.exists () == false)
			if (folder.mkdirs () == false)
				System.out.println (">>> Error al crear la carpeta: " + folder.toString ());
	}

	// Copy input files in 'DocModel' to new working dir with new docType name
	public String copyDocToProjectsDir (DocRecord docRecord) {
		this.createFolder (DocModel.docsPath);
		File sourceFilepath = new File (docRecord.docFilepath);
		File destFilepath = new File (DocModel.docsPath, docRecord.docTypeFilename);
		Utils.copyFile (sourceFilepath.toString (), destFilepath.toString ());
		String docFilepath = Utils.convertToOSPath (destFilepath.toString ());
		return docFilepath;
	}		
}
