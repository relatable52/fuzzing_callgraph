import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.json.JsonSanitizer;

public class JsonSanitizerFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        String input = data.consumeRemainingAsString();
        String output;

        try{
            output = JsonSanitizer.sanitize(input, 10);

            try {
                JsonSanitizer.sanitize(output).equals(output);
            } catch (Exception e) {
            }

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
