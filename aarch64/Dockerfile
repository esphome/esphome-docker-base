# This is an auto-generated file, please edit template/Dockerfile!
FROM arm64v8/ubuntu:bionic

COPY qemu/qemu-aarch64-static /usr/bin/qemu-aarch64-static

RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-pil \
        iputils-ping \
        git \
        curl \
    && rm -rf \
        /tmp/* \
        /var/{cache,log}/* \
        /var/lib/apt/lists/*

# Fix click python3 lang warning https://click.palletsprojects.com/en/7.x/python3/
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

COPY platformio.ini /opt/pio/

RUN \
    pip3 install --no-cache-dir --no-binary :all: platformio==4.0.3 \
    # Change some platformio settings
    && platformio settings set enable_telemetry No \
    && platformio settings set check_libraries_interval 1000000 \
    && platformio settings set check_platformio_interval 1000000 \
    && platformio settings set check_platforms_interval 1000000 \
    # Build an empty platformio project to force platformio to install all fw build dependencies
    # The return-code will be non-zero since there's nothing to build.
    && (platformio run -d /opt/pio; echo "Done") \
    && rm -rf /opt/pio/ \
    \
    && rm -rf /root/.platformio/packages/toolchain-xtensa32 \
    && curl -sSL -o /toolchain-xtensa32.tar.gz \
         https://github.com/esphome/esphome-docker-base/releases/download/v1.4.0/toolchain-xtensa32.tar.gz \
    && tar -xzf /toolchain-xtensa32.tar.gz -C /root/.platformio/packages/ \
    && rm /toolchain-xtensa32.tar.gz \
    \
    && rm -rf /root/.platformio/packages/toolchain-xtensa@1.40802.2 \
    && mkdir /root/.platformio/packages/toolchain-xtensa@1.40802.2 \
    && curl -sSL -o /toolchain-xtensa.tar.gz \
         https://github.com/esphome/esphome-docker-base/releases/download/v1.4.0/toolchain-xtensa.tar.gz \
    && tar -xzf /toolchain-xtensa.tar.gz --strip-components=1 -C /root/.platformio/packages/toolchain-xtensa@1.40802.2 \
    && rm /toolchain-xtensa.tar.gz


VOLUME /config
WORKDIR /usr/src/app
