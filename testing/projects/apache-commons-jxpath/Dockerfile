FROM maven:3.6.3-openjdk-8 AS builder

WORKDIR /build
RUN git clone https://github.com/apache/commons-jxpath.git

WORKDIR /build/commons-jxpath
RUN mvn clean package

FROM scratch

COPY --from=builder /build/commons-jxpath/target/*.jar /repo/
COPY ../../../jazzer-linux/jazzer_standalone.jar /repo/