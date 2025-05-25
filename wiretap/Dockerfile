# Stage 1: Build and run jsoup with Wiretap
FROM maven:3.9-eclipse-temurin-8 as builder

# Install tools
RUN apt-get update && apt-get install -y git ant

# Create working directory
WORKDIR /app

# Clone jsoup
RUN git clone https://github.com/jhy/jsoup.git

# Clone Wiretap at version v0.1.0
RUN git clone --branch v0.1.0 https://github.com/ucla-pls/wiretap.git

# Build Wiretap
WORKDIR /app/wiretap
RUN ant

# Back to jsoup dir
WORKDIR /app/jsoup

# Run tests with Wiretap agent
RUN mvn clean test -DargLine="-javaagent:/app/wiretap/build/wiretap.jar"

# Stage 2: Export only the dynamic callgraph
FROM scratch as export
COPY --from=builder /app/jsoup/target/_wiretap/ /_wiretap/
