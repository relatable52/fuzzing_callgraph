import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;

import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.driver.FuzzedDataProviderImpl;
import com.code_intelligence.jazzer.utils.UnsafeProvider;

public class Entrypoint {
    public static void entrypoint(File inputFile) throws Exception {
        byte[] input = loadInput(inputFile.getAbsolutePath());
        FuzzedDataProviderImpl fuzzedDataProvider = FuzzedDataProviderImpl.withJavaData(input);
        JsonFlattenerFuzzer.fuzzerTestOneInput(fuzzedDataProvider);
    }

    public static byte[] loadInput(String inputFilePath) {
        try {
            return Files.readAllBytes(Paths.get(inputFilePath));
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static void recurseDirectories(File path) throws Exception {
        for (File inputFile : path.listFiles()) {
            if (inputFile.isFile()) {
                entrypoint(inputFile);
            } else {
                recurseDirectories(inputFile);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        recurseDirectories(new File(args[0]));
    }
}
