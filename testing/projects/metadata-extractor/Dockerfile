FROM maven:3.6.3-openjdk-8 AS builder

WORKDIR /build
RUN git clone https://github.com/drewnoakes/metadata-extractor.git metadata-extractor

WORKDIR /build/metadata-extractor
ENV MAVEN_ARGS="-Djavac.src.version=15 -Djavac.target.version=15 -Dmaven.javadoc.skip=true -DskipTests -Dmaven.repo.local=/root/.m2"
RUN mvn package org.apache.maven.plugins:maven-shade-plugin:3.2.4:shade $MAVEN_ARGS

RUN mkdir -p /repo && cp /build/metadata-extractor/target/*.jar /repo/
RUN cp -r /build/metadata-extractor/target/classes /classes

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