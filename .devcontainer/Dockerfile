FROM ubuntu:22.04

RUN apt update && apt install -y \
    build-essential \
    cmake \
    git \
    python3-dev \
    python3-pip \
    wget

RUN pip3 install --upgrade pip

RUN node_version=16.13.0 \
    && wget -q https://nodejs.org/dist/v${node_version}/node-v${node_version}-linux-x64.tar.xz \
    && tar -xf node-v${node_version}-linux-x64.tar.xz \
    && mv node-v${node_version}-linux-x64 /usr/local/lib/nodejs \
    && rm node-v${node_version}-linux-x64.tar.xz \
    && ln -s /usr/local/lib/nodejs/bin/node /usr/local/bin/node \
    && ln -s /usr/local/lib/nodejs/bin/npm /usr/local/bin/npm \
    && ln -s /usr/local/lib/nodejs/bin/npx /usr/local/bin/npx

RUN npm install -g yarn