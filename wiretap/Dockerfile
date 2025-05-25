FROM openjdk:8-jdk

# Install necessary tools
RUN apt-get update && apt-get install -y git maven graphviz

# Set working directory
WORKDIR /app

# Clone jsoup repository
RUN git clone https://github.com/jhy/jsoup.git

# Clone JDCallgraph repository
RUN git clone https://github.com/dkarv/jdcallgraph.git

# Build JDCallgraph
WORKDIR /app/jdcallgraph
RUN mvn install

# Create JDCallgraph configuration file
RUN echo "\
outDir: /app/jsoup/jdcallgraph_output\n\
logLevel: 4\n\
logConsole: true\n\
multiGraph: false\n\
groupBy: THREAD\n\
writeTo: DOT,TRACE\n\
" > config.ini

# Build jsoup with JDCallgraph agent
WORKDIR /app/jsoup
RUN mvn clean test -DargLine="-javaagent:/app/jdcallgraph/target/jdcallgraph.jar=/app/jdcallgraph/config.ini"

# Set default command
CMD ["bash"]
