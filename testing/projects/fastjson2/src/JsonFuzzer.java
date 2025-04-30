import com.alibaba.fastjson2.JSON;
import com.alibaba.fastjson2.JSONException;
import com.code_intelligence.jazzer.api.FuzzedDataProvider;

public class JsonFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        try {
            JSON.parse(data.consumeRemainingAsString());
        } catch (Exception ignored) {
        }
    }
}
