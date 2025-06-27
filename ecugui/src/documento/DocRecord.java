package documento;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.logging.Level;
import java.util.logging.Logger;
import main.Utils;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class DocRecord {
	public String docEmpresa;
	public String docType;
	public String docNumber;
	public String docFilepath;
	public String jsonFilepath;
	public String docTypeFilename;
	public String docFilename;

	public Map<String, Object> mainFields;

	public DocRecord () {
	}

	// Contructor used before processing files
	public DocRecord (String docFilepath, String docEmpresa, String docType, String docNumber) {
		this.docFilepath = docFilepath;
		this.docEmpresa = docEmpresa;
		this.docType = docType;
		this.docNumber = docNumber;

		this.jsonFilepath = null;
		this.mainFields = null;
		this.setWorkingDocName ();
	}

	// Constructor used after processing files
	public DocRecord (DocRecord initRecord, String docFilepath, String jsonFilepath) throws ParseException, IOException {
		this (docFilepath, initRecord.docEmpresa, initRecord.docType, initRecord.docNumber);
		//this.docType = docType.toUpperCase ();
		this.jsonFilepath = jsonFilepath;
		this.mainFields = this.getMainFields ();
	}

	public String getEcufieldsFile () throws FileNotFoundException {
		if (this.jsonFilepath == null)
			throw new FileNotFoundException ("Archivo NULO del registro del documento");
		
		if (this.jsonFilepath.contains ("\\\\"))
			return this.jsonFilepath;
		this.jsonFilepath = Utils.convertToOSPath (this.jsonFilepath);
		return this.jsonFilepath;
	}

	// Set new working doc name used for copying the file documents dir
	public void setWorkingDocName () {
		String docPrefix="", dummyPrefix="", testPrefix = "";
		
		if ("CARTAPORTE".equals (this.docType))
			docPrefix = "-CPI-";
		else if ("MANIFIESTO".equals (this.docType))
			docPrefix = "-MCI-";

		// Get file extension (.pdf)
		int lastDotIndex = docFilepath.lastIndexOf ('.');
		String ext = "." + docFilepath.substring (lastDotIndex + 1);

		// Check if testing session
		if (docFilepath.toUpperCase ().contains ("TEST"))
			testPrefix = "TEST-";
		// Check if dummy document
		if (docFilepath.contains ("DUMMY"))
			dummyPrefix = "DUMMY-";
		docEmpresa = docEmpresa.replace ("::", "_");
		
		this.docTypeFilename = testPrefix+dummyPrefix+docEmpresa+docPrefix+docNumber+ext;
	}

	// Get main fields from procesed file
	public Map getMainFields () throws ParseException, IOException {
		mainFields = new HashMap ();
		// Load JSON mainFields to class mainFields
		JSONParser parser = new JSONParser ();
		try {
			// Get values for record view
			Object obj = parser.parse (new FileReader (jsonFilepath));
			JSONObject jsonObject = (JSONObject) obj;
			Set<String> keys = new TreeSet (jsonObject.keySet ());
			mainFields = getFieldsFromJson (jsonObject);
		} catch (IOException | ParseException ex) {
			throw ex;
		}
		return mainFields;
	}

	public Map getFieldsFromJson (JSONObject json) {
		Map fields = new HashMap ();
		Set<String> keys = new TreeSet (json.keySet ());
		for (String k : keys) {
			String value = json.get (k) == null ? "" : json.get (k).toString ();
			fields.put (k, value);
		}
		return (fields);
	}

	@Override
	public String toString () {
		String out = "docType: " + docType + "\n"
			+ "	docFilepath: " + docFilepath + "\n"
			+ "	jsonFilepath: " + jsonFilepath + "\n"
			+ "	docTypeFilename: " + docTypeFilename + "\n"
			+ "	docFilename: " + docFilename + "\n";
		return out;
	}

	// Return document info: filepath or mainFields after processed
	public String toStringFull () {
		StringBuilder str = new StringBuilder ();

		if (this.jsonFilepath == null)
			str.append (String.format ("DocRecord: docType: %s, docTypeFilename: %s, docFilepath: %s", docType, docTypeFilename, docFilepath));
		else {
			TreeSet<String> keys = new TreeSet (mainFields.keySet ());
			for (String k : keys) {
				str.append (k + ":" + mainFields.get (k) + "\n");
			}
		}
		return (str.toString ());
	}

	public TreeSet<String> getMainKeysSorted () {
		TreeSet<String> ts = new TreeSet (mainFields.keySet ());
		return (ts);
	}

	public void update (String key, String text) {
		String value = text.equals ("") ? null : text;
		mainFields.put (key, value);
	}

	// Write record mainfields to json file
	public void writeToJsonFile (String jsonFilepath) {
		JsonParser jsonParser = new JsonParser ();

		try (FileReader fileReader = new FileReader (jsonFilepath); BufferedReader bufferedReader = new BufferedReader (
			new InputStreamReader (new FileInputStream (jsonFilepath), "UTF-8"))) {
			JsonObject jsonObject = (JsonObject) jsonParser.parse (fileReader).getAsJsonObject ();
			TreeSet<String> keysSet = new TreeSet (jsonObject.keySet ());
			for (String key : keysSet) {
				jsonObject.addProperty (key, (String) mainFields.get (key));
			}
			// Step 3: Write the updated JSON object back to the file
			Gson gson = new GsonBuilder ()
				.setPrettyPrinting ()
				.serializeNulls ()
				.create ();
			try (OutputStream os = new FileOutputStream (jsonFilepath); Writer writer = new OutputStreamWriter (os, "UTF-8")) {
				// Serialize the object to JSON and write it to the file with UTF-8 encoding
				gson.toJson (jsonObject, writer);
			}
		} catch (IOException ex) {
			Logger.getLogger (DocRecord.class.getName ()).log (Level.SEVERE, null, ex);
		}
	}
	
	public String getDocType () {
		return this.docType;
	}
}
