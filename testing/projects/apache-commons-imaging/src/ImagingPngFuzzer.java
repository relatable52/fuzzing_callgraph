import java.io.IOException;
import org.apache.commons.imaging.bytesource.ByteSource;
import org.apache.commons.imaging.formats.png.PngImageParser;

public class ImagingPngFuzzer {
    public static void fuzzerTestOneInput(byte[] input) {
        try {
            new PngImageParser().getBufferedImage(ByteSource.array(input), null);
        } catch (IOException ignored) {
        }
    }
}
