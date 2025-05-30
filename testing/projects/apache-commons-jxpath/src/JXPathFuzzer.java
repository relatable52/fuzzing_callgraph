import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import java.io.StringReader;
import java.io.IOException;

import org.w3c.dom.Document;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.ParserConfigurationException;

import org.apache.commons.jxpath.JXPathContext;
import org.apache.commons.jxpath.JXPathException;

public class JXPathFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        DocumentBuilder builder = null;
        Document doc = null;
        try {
            try {
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                factory.setValidating(data.consumeBoolean());
                factory.setNamespaceAware(data.consumeBoolean());
                factory.setExpandEntityReferences(data.consumeBoolean());
                builder = factory.newDocumentBuilder();
            } catch (Exception parserConfigurationException) {
            }

            try {
                doc = builder.parse(new InputSource(new StringReader(data.consumeString(2000))));
            } catch (SAXException | IOException e) {
            }

            JXPathContext context = JXPathContext.newContext(doc);
            try {
                context.selectNodes(data.consumeRemainingAsString());
            } catch (JXPathException e) {
            }
        } catch (Exception e) {
            return;
        }
    }
}
