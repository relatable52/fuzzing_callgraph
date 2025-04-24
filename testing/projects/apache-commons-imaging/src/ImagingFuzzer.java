public class ImagingFuzzer {
    public static void fuzzerTestOneInput(byte[] input) {
        byte[] bmpInput = input.clone();
        byte[] gifInput = input.clone();
        byte[] jpegInput = input.clone();
        byte[] pngInput = input.clone();
        byte[] tiffInput = input.clone();
        try {
            ImagingBmpFuzzer.fuzzerTestOneInput(bmpInput);
            ImagingGifFuzzer.fuzzerTestOneInput(gifInput);
            ImagingJpegFuzzer.fuzzerTestOneInput(jpegInput);
            ImagingPngFuzzer.fuzzerTestOneInput(pngInput);
            ImagingTiffFuzzer.fuzzerTestOneInput(tiffInput);
        } catch (Exception ignored) {
        }
    }
}
