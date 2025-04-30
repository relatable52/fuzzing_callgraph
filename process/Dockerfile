FROM python:3.12-slim

# Install necessary tools and Just
RUN apt-get update && \
    apt-get install -y curl && \
    curl -Lo /usr/local/bin/just https://github.com/casey/just/releases/latest/download/just-$(uname -m)-unknown-linux-musl && \
    chmod +x /usr/local/bin/just && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt /app
COPY scripts/ /app/scripts/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your justfile into the container
COPY justfile ./

# Set Just as the default command
CMD ["just"]
