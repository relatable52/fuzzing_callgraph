import java.io.IOException;
import org.apache.commons.imaging.bytesource.ByteSource;
import org.apache.commons.imaging.formats.bmp.BmpImageParser;

public class ImagingBmpFuzzer {
    public static void fuzzerTestOneInput(byte[] input) {
        try {
            new BmpImageParser().getBufferedImage(ByteSource.array(input), null);
        } catch (IOException ignored) {
        }
    }
}
