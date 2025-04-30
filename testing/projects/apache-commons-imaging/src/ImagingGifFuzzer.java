import java.io.IOException;
import org.apache.commons.imaging.bytesource.ByteSource;
import org.apache.commons.imaging.formats.gif.GifImageParser;

public class ImagingGifFuzzer {
    public static void fuzzerTestOneInput(byte[] input) {
        try {
            new GifImageParser().getBufferedImage(ByteSource.array(input), null);
        } catch (IOException ignored) {
        }
    }
}
