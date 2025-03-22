FROM maven:3.6.3-openjdk-8 AS builder

WORKDIR /build
COPY . .
RUN mvn dependency:go-offline