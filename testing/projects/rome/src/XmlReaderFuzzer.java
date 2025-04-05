import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import java.io.IOException;
import java.io.ByteArrayInputStream;
import com.rometools.rome.io.XmlReader;
import com.rometools.rome.io.FeedException;
import com.rometools.rome.io.SyndFeedInput;
import com.rometools.rome.feed.synd.SyndFeed;
import java.lang.IllegalArgumentException;

public class XmlReaderFuzzer {
  public static void fuzzerTestOneInput(FuzzedDataProvider data) {
    ByteArrayInputStream bais = new ByteArrayInputStream(data.consumeRemainingAsBytes());
    try{
      SyndFeed feed = new SyndFeedInput().build(new XmlReader(bais));
    }
    catch( Exception e){
      return;
    }
  
  }
}