FROM maven:3.6.3-openjdk-8 AS builder

WORKDIR /build
RUN git clone https://github.com/OWASP/json-sanitizer.git

WORKDIR /build/json-sanitizer
RUN mkdir -p /out
RUN mvn package
RUN CURRENT_VERSION=$(mvn org.apache.maven.plugins:maven-help-plugin:3.2.0:evaluate \
-Dexpression=project.version -q -DforceStdout) && cp "target/json-sanitizer-$CURRENT_VERSION.jar" /out/json-sanitizer.jar

RUN mvn dependency:copy -Dartifact=com.google.code.gson:gson:2.8.6 -DoutputDirectory=/out/

RUN mkdir -p /repo && cp /out/*.jar /repo/
RUN cp -r /build/jsoup/target/classes /classes

COPY --from=jazzer jazzer_standalone.jar /repo/
COPY --from=jazzer libunsafe_provider.jar /repo/

RUN mkdir -p /build/fuzzer /build/fuzzer/target
WORKDIR /build/fuzzer
RUN --mount=type=bind,source=src/,target=src/ \
    javac -source 8 -target 8 -cp "/repo/*" -d target src/*.java && \
    jar cf /repo/fuzzer.jar -C target . && \
    rm -rf target

FROM scratch
COPY --from=builder /repo/ /repo/
COPY --from=builder /classes/ /classes/