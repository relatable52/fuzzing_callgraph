import java.io.*;
import java.nio.charset.StandardCharsets;

import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;

import com.itextpdf.kernel.pdf.PdfReader;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.io.exceptions.*;

public class PdfFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        try {
            InputStream stream = new ByteArrayInputStream(data.consumeRemainingAsString().getBytes(StandardCharsets.UTF_8));
            PdfReader reader = new PdfReader(stream);
            PdfDocument pdfDoc = new PdfDocument(reader);
        } catch (Exception e) { }
    }
}