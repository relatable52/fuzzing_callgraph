import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import java.io.*;
import java.util.Enumeration;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import java.lang.IllegalArgumentException;
import java.lang.StringIndexOutOfBoundsException;

import org.zeroturnaround.zip.ZipUtil;
import org.zeroturnaround.zip.ZipException;
import org.zeroturnaround.zip.commons.IOUtils;


class UnpackFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        String str = data.consumeString(100);
        String dir = "/tmp";
        int level = data.consumeInt();
        InputStream is = new ByteArrayInputStream(data.consumeRemainingAsBytes());

        try {
            ZipUtil.unpackEntry(is, str);
            ZipUtil.unpack(is, new File(dir));
            ZipUtil.unwrap(is, new File(dir));
            ZipUtil.repack(is, new File(dir), level);
            IOUtils.closeQuietly(is);
        } catch (Exception e) {
        } 
    }
}