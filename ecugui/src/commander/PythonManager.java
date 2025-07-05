/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package commander;

import documento.DocModel;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

public class PythonManager {

    private static PythonManager instance;
    private Process pythonProcess;
    private BufferedWriter pythonInput;
    private BufferedReader pythonOutput;
    private BufferedReader pythonError;

    private PythonManager() throws IOException {
        startPythonProcess();
    }

    public static synchronized PythonManager getInstance() throws IOException {
        if (instance == null) {
            instance = new PythonManager();
        }
        return instance;
    }

    private void startPythonProcess() throws IOException {
        try {
            ArrayList<String> commandList = this.createExecutableCommand();
            ProcessBuilder pb = new ProcessBuilder(commandList);
            pythonProcess = pb.start();
            pythonInput = new BufferedWriter(new OutputStreamWriter(pythonProcess.getOutputStream(), "UTF-8"));
            pythonOutput = new BufferedReader(new InputStreamReader(pythonProcess.getInputStream(), "UTF-8"));
            pythonError = new BufferedReader(new InputStreamReader(pythonProcess.getErrorStream(), "UTF-8"));

            String readyMessage = pythonOutput.readLine();
            System.out.println("+++ Starting message: " + readyMessage);
            if (!readyMessage.contains("Python executable is ready to receive commands")) {
                throw new IOException("Python process did not initialize properly.");
            }
        } catch (Exception ex) {
            Logger.getLogger(PythonWorker.class.getName()).log(Level.SEVERE, null, ex);
            //String line = pythonError.readLine();
            System.out.println("+++ pythonError: " + pythonError);
        }
    }

    public synchronized String sendCommandSync(String service, String param1, String param2, String param3, String param4) throws IOException {
        String command = service + "|" + param1 + "|" + param2 + "|" + param3 + "|" + param4;
        System.out.print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
        System.out.print(" JCommand: ");
        System.out.println("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<");
        System.out.println(command);
        System.out.println(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<");
        pythonInput.write(command + "\n");
        pythonInput.flush();

        String response = null;
        do {
            response = pythonOutput.readLine();
        } while (!response.startsWith("RESPONSE:"));

        return response;
    }

    public void shutdown() throws IOException {
        sendCommandSync("exit", "", "", "", "");
        pythonProcess.destroy();
    }

    // Create command list according to the OS, service, and parameters
    public ArrayList<String> createExecutableCommand() {
        ArrayList<String> commandList = null;
        String OS = System.getProperty("os.name").toLowerCase();
        String separator = OS.contains("windows") ? "\\" : "/";
        String runningPath = DocModel.runningPath;

        // For testing: python .py, for production: windows .exe
        String exeProgram = "ecuapass_commander" + separator + "ecuapass_commander.exe";
        String pyProgram = "commander" + separator + "ecuapass_commander.py";

        String command = "";
        String basepath = Paths.get(runningPath).getFileName().toString();
        if (OS.contains("windows") && "test".equals(basepath)) {
            command = Paths.get(runningPath, pyProgram).toString();
            commandList = new ArrayList<>(Arrays.asList("cmd.exe", "/c", "python", command));
        } else if (OS.contains("windows")) {
            command = Paths.get(runningPath, exeProgram).toString();
            commandList = new ArrayList<>(Arrays.asList(command));
        } else if (OS.contains("linux")) {
            command = Paths.get(runningPath, pyProgram).toString();
            commandList = new ArrayList<>(Arrays.asList("python3", command, runningPath));
        }

        System.out.println("+++ commandList: " + commandList);
        return commandList;
    }
}
