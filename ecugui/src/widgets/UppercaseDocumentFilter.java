package widgets;

//---------------------------------------------------------------------------------------

import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.DocumentFilter;

// Class for allow only upercase to DocNumberField
//---------------------------------------------------------------------------------------
public class UppercaseDocumentFilter extends DocumentFilter {
	@Override
	public void replace (DocumentFilter.FilterBypass fb, int offset, int length, String str, AttributeSet attr)
		throws BadLocationException {
		super.replace (fb, offset, length, str != null ? str.toUpperCase () : null, attr);
	}
}

