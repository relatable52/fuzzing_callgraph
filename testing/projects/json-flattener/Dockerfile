FROM maven:3.6.3-openjdk-11 AS builder

WORKDIR /build
RUN git clone https://github.com/wnameless/json-flattener.git

WORKDIR /build/json-flattener
ENV MAVEN_ARGS="-Djavac.src.version=11 -Djavac.target.version=11 -DskipTests -Dgpg.skip"
RUN mkdir -p /out
RUN mvn package org.apache.maven.plugins:maven-shade-plugin:3.2.4:shade $MAVEN_ARGS

RUN cp /build/json-flattener/target/*.jar /repo/
RUN cp -r /build/json-flattener/target/classes /classes

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