FROM maven:3.6.3-openjdk-11 AS builder

# Arguments
ARG PROJECT=zt-zip
ARG MAIN_REPO=https://github.com/zeroturnaround/zt-zip.git

WORKDIR /build

# Clone project
RUN git clone $MAIN_REPO $PROJECT

WORKDIR /build/$PROJECT

# Optional: Checkout a known stable version
RUN git checkout tags/zt-zip-1.16

# Build with Maven using Java 11
ENV MAVEN_ARGS="-Djavac.src.version=11 -Djavac.target.version=11 -DskipTests"
RUN mvn package org.apache.maven.plugins:maven-shade-plugin:3.2.4:shade $MAVEN_ARGS

# Extract version and copy jar + classes
RUN CURRENT_VERSION=$(mvn org.apache.maven.plugins:maven-help-plugin:3.2.0:evaluate \
  -Dexpression=project.version -q -DforceStdout) && \
  mkdir -p /output && \
  cp target/zt-zip-${CURRENT_VERSION}.jar /output/zt-zip.jar 
RUN mkdir -p /classes && cp -r target/classes/* /classes/

RUN mkdir -p /repo && cp /output/*.jar /repo/
RUN cp -r /build/zt-zip/target/classes /classes

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