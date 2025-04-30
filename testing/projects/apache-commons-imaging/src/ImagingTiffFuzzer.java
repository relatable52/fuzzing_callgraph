import java.io.IOException;
import org.apache.commons.imaging.bytesource.ByteSource;
import org.apache.commons.imaging.formats.tiff.TiffImageParser;

public class ImagingTiffFuzzer {
    public static void fuzzerTestOneInput(byte[] input) {
        try {
            new TiffImageParser().getBufferedImage(ByteSource.array(input), null);
        } catch (IOException ignored) {
        }
    }
}
