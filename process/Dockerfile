# Use a lightweight Haskell base image
FROM haskell:9.2

# Install system dependencies and Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt

# Clone the javaq repository
RUN git clone https://github.com/ucla-pls/javaq.git

# Build and install javaq
WORKDIR /opt/javaq
RUN stack setup && stack install

# Add Stack's local bin to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Set default command to bash
CMD ["/bin/bash"]
