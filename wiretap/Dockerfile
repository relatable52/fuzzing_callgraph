# Use an official Maven image as the base
FROM maven:3.8.5-openjdk-17 as builder

# Set the working directory
WORKDIR /app

# Clone the jsoup repository
RUN git clone https://github.com/jhy/jsoup.git
WORKDIR /app/jsoup

# Download the JDCallgraph agent
COPY ./jdcallgraph-0.1-agent.jar /app/jsoup/jdcallgraph-agent.jar

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
