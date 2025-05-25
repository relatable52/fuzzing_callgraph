# Use an official Maven image as the base
FROM openjdk:17-jdk-slim as builder

# Set the working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y git wget

# Clone the jsoup repository
RUN git clone https://github.com/jhy/jsoup.git
WORKDIR /app/jsoup

# Download the JDCallgraph agent
RUN wget -O jdcallgraph-agent.jar https://github.com/dkarv/jdcallgraph/releases/download/combined-0.1.5/jdcallgraph-0.1-agent.jar

# Create the JDCallgraph configuration file
RUN echo "\
outDir: /app/jsoup/jdcallgraph_output\n\
logLevel: 4\n\
logConsole: true\n\
multiGraph: false\n\
groupBy: THREAD\n\
writeTo: DOT,TRACE\n\
" > config.ini

# Run Maven tests with the JDCallgraph agent
RUN mvn clean test -DargLine="-javaagent:/app/jsoup/jdcallgraph-agent.jar=/app/jsoup/config.ini"

FROM scratch as export
COPY --from=builder /app/jsoup/jdcallgraph_output /jdcallgraph_output
