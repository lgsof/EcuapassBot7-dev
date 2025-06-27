package exceptions;

public class EcuapassExceptions {

	public static class SettingsError extends Exception {
		public SettingsError (String message) {
			super (message);
		}
	}

	public static class ConnectionError extends Exception {

		public ConnectionError (String message) {
			super (message);
		}
	}

	public static class PdfDocError extends Exception {

		public PdfDocError (String message) {
			super (message);
		}
	}

	public static class AppDocAccessError extends Exception {

		public AppDocAccessError (String message) {
			super (message);
		}
	}

}
