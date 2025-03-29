import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.json.JsonSanitizer;

public class JsonSanitizerFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        String input = data.consumeRemainingAsString();
        String output;

        try{
            try {
                output = JsonSanitizer.sanitize(input, 10);
            } catch (ArrayIndexOutOfBoundsException e) {
                // ArrayIndexOutOfBoundsException is expected if nesting depth is
                // exceeded.
            }

            try {
                JsonSanitizer.sanitize(output).equals(output);
            } catch (Exception e) {
            }

            // Check that the output is valid JSON. Invalid JSON may crash other parts
            // of the application that trust the output of the sanitizer.
            try {
                Gson gson = new Gson();
                gson.fromJson(output, JsonElement.class);
            } catch (Exception e) {
            }
        } catch (Exception e) {
            return;
        }
    }
}
