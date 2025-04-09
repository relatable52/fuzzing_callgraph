FROM gradle:7.6.4-jdk8 AS builder

WORKDIR /build
RUN git clone --branch version-2.1.4 https://github.com/dom4j/dom4j.git

WORKDIR /build/dom4j
RUN ./gradlew -x test build

RUN mkdir -p /repo && cp build/libs/dom4j.jar /repo/dom4j.jar
RUN cp -r build/classes/java/main /classes

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