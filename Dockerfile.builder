FROM homeassistant/amd64-base-ubuntu:16.04

ENV LANG C.UTF-8

# Install docker
# https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
RUN apt-get update && apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && add-apt-repository "deb https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
    && apt-get update && apt-get install -y docker-ce \
    && rm -rf /var/lib/apt/lists/*

# setup arm binary support
RUN apt-get update && apt-get install -y \
        qemu-user-static \
        binfmt-support \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /data
