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
    parallel \
    golang-go \
    php-cli \
    php-mbstring \
    php-json \
    php-curl \
    php-zip \
    unzip \
    curl \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Python libs and transliteration
RUN pip3 install --break-system-packages --no-cache-dir \
    Levenshtein==0.27.3 \
    tabulate==0.10.0 \
    srtools==0.1.13 \
    cyrtranslit \
    git+https://github.com/Serbian-AI-Society/SrbAI.git

COPY ./scripts /tmp/scripts

# Go transliteration
RUN ./tmp/scripts/eevan78_translit.sh

# Javascript transliteration
RUN npm install -g \
    yuconv-cli \
    @exvorn/serbian-transliteration \
    https://github.com/ivebe/CyrLatConverter.git \
    @pionir/preslovljivac \
    pravopis \
    serbian-script-converter
ENV NODE_PATH=/usr/local/lib/node_modules


# PHP transliteration
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN composer require turanjanin/serbian-transliterator


# Rust transliteration
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cargo install translitrs --root /usr/local


# Set default command
CMD ["/bin/bash"]
