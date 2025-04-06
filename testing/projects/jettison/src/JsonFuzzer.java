import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import org.codehaus.jettison.json.JSONObject;
import org.codehaus.jettison.json.JSONException;

public class JsonFuzzer {
  public static void fuzzerTestOneInput(FuzzedDataProvider data) {
    try{
      JSONObject obj = new JSONObject(data.consumeRemainingAsString());
    }
    catch (Exception e){
      return;
    }
  }
}