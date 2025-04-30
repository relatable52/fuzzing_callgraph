import java.io.IOException;
import org.apache.commons.imaging.bytesource.ByteSource;
import org.apache.commons.imaging.formats.jpeg.JpegImageParser;

public class ImagingJpegFuzzer {
    public static void fuzzerTestOneInput(byte[] input) {
        try {
            new JpegImageParser().getBufferedImage(ByteSource.array(input), null);
        } catch (IOException ignored) {
        }
    }
}
