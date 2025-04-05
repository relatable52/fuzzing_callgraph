FROM maven:3.6.3-openjdk-11 AS builder

WORKDIR /build
RUN git clone https://github.com/srikanth-lingala/zip4j.git zip4j

WORKDIR /build/zip4j
ENV MAVEN_ARGS="-Dmaven.test.skip=true -Djavac.src.version=15 -Djavac.target.version=15"
RUN mkdir -p /out
RUN mvn package org.apache.maven.plugins:maven-shade-plugin:3.2.4:shade $MAVEN_ARGS
RUN CURRENT_VERSION=$(mvn org.apache.maven.plugins:maven-help-plugin:3.2.0:evaluate \
-Dexpression=project.version -q -DforceStdout) && cp target/zip4j-$CURRENT_VERSION.jar /out/zip4j.jar

RUN mkdir -p /repo && cp /out/zip4j.jar /repo/zip4j.jar
RUN cp -r /build/rome/target/classes /classes

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