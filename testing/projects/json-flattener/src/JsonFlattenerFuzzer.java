import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import com.github.wnameless.json.flattener.*;
import com.github.wnameless.json.base.JsonCore;
import com.github.wnameless.json.base.GsonJsonCore;
import com.github.wnameless.json.base.JacksonJsonCore;
import com.github.wnameless.json.unflattener.JsonUnflattener;
import com.github.wnameless.json.unflattener.JsonUnflattenerFactory;

import java.util.function.Consumer;

public class JsonFlattenerFuzzer {
    static PrintMode [] printModes = {PrintMode.PRETTY, PrintMode.MINIMAL};
    static FlattenMode [] flattenModes = {FlattenMode.NORMAL, FlattenMode.MONGODB, FlattenMode.KEEP_ARRAYS, FlattenMode.KEEP_PRIMITIVE_ARRAYS};
    static StringEscapePolicy [] stringEscapePolicies = {StringEscapePolicy.DEFAULT, StringEscapePolicy.ALL, StringEscapePolicy.ALL_BUT_SLASH, StringEscapePolicy.ALL_BUT_UNICODE, StringEscapePolicy.ALL_BUT_SLASH_AND_UNICODE};
    static JsonCore [] jsonCores = {new GsonJsonCore(), new JacksonJsonCore()};

    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        try {
            JsonFlattenerFactory jsonFlattenerFactory = jsonFlattenerFactory(data.pickValue(printModes), data.pickValue(flattenModes), data.pickValue(stringEscapePolicies), data.pickValue(jsonCores));
            JsonUnflattenerFactory jsonUnflattenerFactory = jsonUnflattenerFactory(data.pickValue(printModes), data.pickValue(flattenModes), data.pickValue(jsonCores));
            String json = data.consumeRemainingAsString();
            
            try {
                JsonFlattener jf = jsonFlattenerFactory.build(json);

                jf.flatten();
                jf.flattenAsMap();
            } catch (Exception e) {}
            
            try {
                JsonUnflattener ju = jsonUnflattenerFactory.build(json);

                ju.unflatten();
                ju.unflattenAsMap();
            } catch (Exception e) {}
        } catch (RuntimeException e) {
            // Need to catch it to let fuzzer find initeresting findings.
        }
    }

    static JsonFlattenerFactory jsonFlattenerFactory(PrintMode pm, FlattenMode fm, StringEscapePolicy sep, JsonCore<?> jc) {
        Consumer<JsonFlattener> configurer = jf -> jf.withPrintMode(pm).withFlattenMode(fm).withStringEscapePolicy(sep);

        return new JsonFlattenerFactory(configurer, jc);
    }

    static JsonUnflattenerFactory jsonUnflattenerFactory(PrintMode pm, FlattenMode fm, JsonCore<?> jc) {
        Consumer<JsonUnflattener> configurer = ju -> ju.withPrintMode(pm).withFlattenMode(fm);

        return new JsonUnflattenerFactory(configurer, jc);
    }
}
