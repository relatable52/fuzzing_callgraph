import com.code_intelligence.jazzer.api.BugDetectors;
import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import org.dom4j.io.DOMReader;
import java.io.IOException;
import org.xml.sax.SAXException;
import javax.xml.parsers.ParserConfigurationException;
import java.lang.IllegalArgumentException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.ByteArrayInputStream;
import java.util.List;

public class DOMReaderFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {

        try (AutoCloseable ignored = BugDetectors.allowNetworkConnections()) {

            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder;
            org.w3c.dom.Document doc;

            try {
                builder = factory.newDocumentBuilder();
            } catch (ParserConfigurationException e) {
                return;
            }

            try {
                doc = builder.parse(new ByteArrayInputStream(data.consumeRemainingAsBytes()));
            } catch (SAXException | IOException e) {
                return;
            }

            DOMReader reader = new DOMReader();

            try {
                reader.read(doc);
            } catch (IllegalArgumentException e) {
                return;
            }
        } catch (Exception e) {
            return;
        }
    }
}
