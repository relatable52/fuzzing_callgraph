import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import org.jsoup.Jsoup;
import org.jsoup.Jsoup;
import org.jsoup.parser.Parser;

public class JsoupFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        String input = data.consumeRemainingAsString();
        
        try{
            Jsoup.parse(input);
        } catch (Exception e) {}

        try{
            Jsoup.parse(input, "", Parser.xmlParser());
        } catch (Exception e) {}
    }
}
