FROM maven:3.6.3-openjdk-8 AS builder

WORKDIR /build
RUN git clone https://github.com/apache/commons-jxpath.git

WORKDIR /build/commons-jxpath
ENV MAVEN_ARGS="-Djavac.src.version=15 -Djavac.target.version=15 -DskipTests"
RUN mvn package org.apache.maven.plugins:maven-shade-plugin:3.2.4:shade $MAVEN_ARGS

RUN mkdir -p /repo && cp /build/commons-jxpath/target/*.jar /repo/ && cp /build/commons-jxpath/target/classes /classes

COPY --from=jazzer jazzer_standalone.jar /repo/

RUN mkdir -p /build/fuzzer /build/fuzzer/target
WORKDIR /build/fuzzer
RUN --mount=type=bind,source=src/,target=src/ \
    javac -source 8 -target 8 -cp "/repo/*" -d target src/*Fuzzer.java && \
    jar cf /repo/fuzzer.jar -C target . && \
    rm -rf target

FROM scratch
COPY --from=builder /repo/ /repo/
COPY --from=builder /classes/ /classes/