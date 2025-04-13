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
RUN mvn install $MAVEN_ARGS

# Extract version and copy jar + classes
RUN CURRENT_VERSION=$(mvn org.apache.maven.plugins:maven-help-plugin:3.2.0:evaluate \
  -Dexpression=project.version -q -DforceStdout) && \
  mkdir -p /output && \
  cp target/zt-zip-${CURRENT_VERSION}.jar /output/zt-zip.jar 
RUN mkdir -p /classes && cp -r target/classes/* /classes/