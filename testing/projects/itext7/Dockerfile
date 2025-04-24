FROM maven:3.6.3-openjdk-8 AS builder

ARG PROJECT=itext
ARG MAIN_REPO=https://github.com/itext/itext-java.git
ARG VERSION_TAG=7.2.6

WORKDIR /build

# Clone the full repo
RUN git clone $MAIN_REPO $PROJECT
WORKDIR /build/$PROJECT

# Checkout the desired version tag
RUN git checkout tags/$VERSION_TAG

# Only build the kernel module (skip tests for speed)
ENV MAVEN_ARGS="-DskipTests -Dmaven.javadoc.skip=true"
RUN mvn -pl kernel install $MAVEN_ARGS

# Create a temporary Maven project with a shade plugin to fat-jar the kernel
RUN echo '<project xmlns="http://maven.apache.org/POM/4.0.0" \
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"> \
<modelVersion>4.0.0</modelVersion> \
<groupId>com.itextpdf</groupId><artifactId>kernel-fatjar</artifactId><version>1.0</version> \
<dependencies><dependency><groupId>com.itextpdf</groupId><artifactId>kernel</artifactId><version>'"$VERSION_TAG"'</version></dependency></dependencies> \
<build><plugins><plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-shade-plugin</artifactId><version>3.2.4</version> \
<executions><execution><phase>package</phase><goals><goal>shade</goal></goals></execution></executions> \
</plugin></plugins></build></project>' > kernel-fatjar-pom.xml

# Package the fat jar
RUN mkdir -p /out
RUN mvn -f kernel-fatjar-pom.xml package $MAVEN_ARGS && \
    cp target/kernel-fatjar-1.0.jar /out/itext7.jar

# Copy compiled classes
RUN mkdir -p /classes && cp -r kernel/target/classes/* /classes/

# Fake jazzer jars for compatibility
COPY --from=jazzer jazzer_standalone.jar /repo/
COPY --from=jazzer libunsafe_provider.jar /repo/
RUN cp /out/itext7.jar /repo/

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
