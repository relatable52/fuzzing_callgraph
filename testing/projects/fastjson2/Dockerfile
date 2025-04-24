FROM maven:3.6.3-openjdk-8 AS builder

WORKDIR /build
RUN git clone -b 2.0.57 https://github.com/alibaba/fastjson2.git fastjson2

ENV MAVEN_ARGS="-Dmaven.test.skip=true -Djdk.version=8"

WORKDIR /build/fastjson2
RUN mkdir -p /out
RUN mvn package $MAVEN_ARGS
RUN CURRENT_VERSION=$(mvn org.apache.maven.plugins:maven-help-plugin:3.2.0:evaluate \
-Dexpression=project.version -q -DforceStdout) && cp core/target/fastjson2-$CURRENT_VERSION.jar /out/fastjson2.jar

RUN mkdir -p /repo && cp /out/*.jar /repo/
RUN cp -r /build/fastjson2/core/target/classes /classes

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