FROM maven:3.6.3-openjdk-8 AS builder

WORKDIR /build
RUN git clone -b woodstox-core-7.1.0 https://github.com/FasterXML/woodstox.git

WORKDIR /build/woodstox
ENV MAVEN_ARGS="-Djavac.src.version=15 -Djavac.target.version=15 -DskipTests"
RUN mkdir -p /out
RUN mvn package org.apache.maven.plugins:maven-shade-plugin:3.2.4:shade $MAVEN_ARGS
RUN CURRENT_VERSION=$(mvn org.apache.maven.plugins:maven-help-plugin:3.2.0:evaluate \
-Dexpression=project.version -q -DforceStdout) && cp target/woodstox-core-$CURRENT_VERSION.jar /out/woodstox.jar

RUN mkdir -p /repo && cp /out/*.jar /repo/
RUN cp -r /build/woodstox/target/classes /classes

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
