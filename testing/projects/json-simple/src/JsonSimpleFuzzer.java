import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.io.*;

public class JsonSimpleFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        String fuzzingString = data.consumeRemainingAsString();
        try{
            JSONObject srcObj = new JSONObject();
            srcObj.put("item1", fuzzingString);
            
            StringWriter out = new StringWriter();
            srcObj.writeJSONString(out);
            String jsonText = out.toString();

            StringReader in = new StringReader(jsonText);
            JSONParser parser = new JSONParser();
            JSONObject destObj = (JSONObject)parser.parse(in);

            if (!destObj.equals(srcObj)) {
                throw new IllegalStateException("Decoded object: "
                 + destObj.toString() + " doesn't match original object: " + srcObj.toString());
            }            
        } catch (Exception e) {}

        try {
            JSONParser parser = new JSONParser();
            JSONObject jsonObj = (JSONObject)parser.parse(fuzzingString);
        } catch (Exception e) {}
    }
}
