import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

import de.siegmar.fastcsv.reader.CsvReader;

public class CsvReaderFuzzer {
  public static void fuzzerTestOneInput(FuzzedDataProvider data) {
    byte[] input = data.consumeRemainingAsBytes();
    try {
      CsvReader.builder()
        .ofCsvRecord(new InputStreamReader(new ByteArrayInputStream(input), StandardCharsets.UTF_8))
        .stream()
        .toList();
    } catch (Exception e) {
      // Ignore exceptions
    }
  }
}
