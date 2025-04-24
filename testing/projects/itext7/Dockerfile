FROM maven:3.6.3-openjdk-8 AS builder

# Clone target
ARG MAIN_REPO=https://github.com/itext/itext-java.git
ARG MODULE=kernel
ARG VERSION_TAG=7.2.5

WORKDIR /build

# Clone the full iText repo
RUN git clone $MAIN_REPO itext7
WORKDIR /build/itext7

# Checkout the specific tag
RUN git checkout tags/${VERSION_TAG}

# Overwrite the kernel module's pom.xml with your custom one
COPY src/pom.xml ./${MODULE}/pom.xml

# Build the fat jar
ENV MAVEN_ARGS="-DskipTests -Dmaven.javadoc.skip=true"
RUN mvn -pl ${MODULE} package org.apache.maven.plugins:maven-shade-plugin:3.2.4:shade $MAVEN_ARGS

# Extract fat jar and classes
RUN CURRENT_VERSION=$(mvn -pl ${MODULE} org.apache.maven.plugins:maven-help-plugin:3.2.0:evaluate \
  -Dexpression=project.version -q -DforceStdout) && \
  mkdir -p /repo && \
  cp ${MODULE}/target/*.jar /repo/

RUN mkdir -p /classes && cp -r ${MODULE}/target/classes/* /classes/

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
