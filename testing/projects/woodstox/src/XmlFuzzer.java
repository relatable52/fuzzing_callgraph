import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import java.io.ByteArrayInputStream;
import javax.xml.stream.*;
import com.ctc.wstx.stax.WstxInputFactory;
import com.ctc.wstx.exc.WstxLazyException;

public class XmlFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        WstxInputFactory STAX_F = new WstxInputFactory();
        try {
            XMLStreamReader sr = STAX_F.createXMLStreamReader(new ByteArrayInputStream(data.consumeRemainingAsBytes()));
            streamThrough(sr);
            sr.close();
        } catch (Exception e) {
        }
    }

    public static int streamThrough(XMLStreamReader sr) throws XMLStreamException {
        int result = 0;

        while (sr.hasNext()) {
            int type = sr.next();
            result += type;
            if (sr.hasText()) {
                result += getText(sr).hashCode();
            }
            if (sr.hasName()) {
                result += sr.getName().hashCode();
            }
        }

        return result;
    }

    public static String getText(XMLStreamReader sr) {
        int type = sr.getEventType();
        int expLen = sr.getTextLength();
        String text = sr.getText();
        char[] textChars = sr.getTextCharacters();
        int start = sr.getTextStart();

        return text;
    }
}
