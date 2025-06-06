FROM maven:3.6.3-openjdk-8 AS builder

WORKDIR /build
RUN git clone -b v2.9.0 https://github.com/srikanth-lingala/zip4j.git zip4j

WORKDIR /build/zip4j
ENV MAVEN_ARGS="-Dmaven.test.skip=true -Djavac.src.version=8 -Djavac.target.version=8"
ENV MAVEN_ARGS=$MAVEN_ARGS" -Dmaven.wagon.httpconnectionManager.ttlSeconds=120"
ENV MAVEN_ARGS=$MAVEN_ARGS" -Dmaven.wagon.http.retryHandler.requestSentEnabled=true"
ENV MAVEN_ARGS=$MAVEN_ARGS" -Dmaven.wagon.http.retryHandler.count=5"
RUN mkdir -p /out
COPY pom.xml /build/zip4j/pom.xml
RUN mvn package org.apache.maven.plugins:maven-shade-plugin:3.2.4:shade $MAVEN_ARGS
RUN CURRENT_VERSION=$(mvn org.apache.maven.plugins:maven-help-plugin:3.2.0:evaluate \
-Dexpression=project.version -q -DforceStdout) && cp target/zip4j-$CURRENT_VERSION.jar /out/zip4j.jar

RUN mkdir -p /repo && cp /out/zip4j.jar /repo/zip4j.jar
RUN cp -r /build/zip4j/target/classes /classes

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
