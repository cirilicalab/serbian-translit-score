# Use the latest LTS minimal image
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-pip \
    ruby \
    ruby-dev \
    wget \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages --no-cache-dir \
    Levenshtein==0.27.3 \
    tabulate==0.10.0 \
    srtools==0.1.13 \
    cyrtranslit \
    git+https://github.com/Serbian-AI-Society/SrbAI.git


# Set default command
CMD ["/bin/bash"]
