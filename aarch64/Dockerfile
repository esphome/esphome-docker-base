# This is an auto-generated file, please edit template/Dockerfile!
FROM arm64v8/ubuntu:bionic

COPY qemu/qemu-aarch64-static /usr/bin/qemu-aarch64-static

RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        python \
        python-pip \
        python-setuptools \
        python-pil \
        iputils-ping \
        git \
        curl \
    && rm -rf \
        /tmp/* \
        /var/{cache,log}/* \
        /var/lib/apt/lists/*

COPY platformio.ini /opt/pio/

RUN \
    pip2 install --no-cache-dir --no-binary :all: platformio==3.6.7 \
    # Change some platformio settings
    && platformio settings set enable_telemetry No \
    && platformio settings set check_libraries_interval 1000000 \
    && platformio settings set check_platformio_interval 1000000 \
    && platformio settings set check_platforms_interval 1000000 \
    # Build an empty platformio project to force platformio to install all fw build dependencies
    # The return-code will be non-zero since there's nothing to build.
    && (platformio run -d /opt/pio; echo "Done") \
    && rm -rf /opt/pio/


RUN \
    curl -sSL -o /toolchain-xtensa32.tar.gz \
        https://github.com/esphome/esphome-docker-base/releases/download/v1.4.0/toolchain-xtensa32.tar.gz \
    && tar -xzvf /toolchain-xtensa32.tar.gz -C /root/.platformio/packages/ \
    && rm /toolchain-xtensa32.tar.gz \
    \
    && curl -sSL -o /toolchain-xtensa.tar.gz \
        https://github.com/esphome/esphome-docker-base/releases/download/v1.4.0/toolchain-xtensa.tar.gz \
    && tar -xzvf /toolchain-xtensa.tar.gz -C /root/.platformio/packages/ \
    && rm /toolchain-xtensa.tar.gz


VOLUME /config
WORKDIR /usr/src/app
