FROM maven:3.6.3-openjdk-11 AS builder

WORKDIR /build
RUN git clone -b json-flattener-0.16.0 https://github.com/wnameless/json-flattener.git

WORKDIR /build/json-flattener
ENV MAVEN_ARGS="-Djavac.src.version=8 -Djavac.target.version=8 -DskipTests -Dgpg.skip \
-Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8 -Dmaven.compiler.release=8"
RUN mkdir -p /out
RUN mvn package org.apache.maven.plugins:maven-shade-plugin:3.2.4:shade $MAVEN_ARGS
RUN CURRENT_VERSION=$(mvn org.apache.maven.plugins:maven-help-plugin:3.2.0:evaluate \
-Dexpression=project.version -q -DforceStdout) && cp target/json-flattener-$CURRENT_VERSION.jar /out/json-flattener.jar

RUN mvn dependency:copy -Dartifact=com.google.code.gson:gson:2.8.6 -DoutputDirectory=/out/

RUN mkdir -p /repo && cp /out/*.jar /repo/
RUN cp -r /build/json-flattener/target/classes /classes

COPY --from=jazzer jazzer_standalone.jar /repo/
COPY --from=jazzer libunsafe_provider.jar /repo/

FROM maven:3.6.3-openjdk-8 AS fuzzer

COPY --from=builder /repo/*.jar /repo/

RUN mkdir -p /build/fuzzer /build/fuzzer/target
WORKDIR /build/fuzzer
RUN --mount=type=bind,source=src/,target=src/ \
    javac -source 8 -target 8 -cp "/repo/*" -d target src/*.java && \
    jar cf /repo/fuzzer.jar -C target . && \
    rm -rf target

FROM scratch
COPY --from=fuzzer /repo/ /repo/
COPY --from=builder /classes/ /classes/