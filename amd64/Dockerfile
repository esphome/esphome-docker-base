# This is an auto-generated file, please edit template/Dockerfile!
FROM amd64/ubuntu:bionic



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
    pip3 install --no-cache-dir --no-binary :all: platformio==4.3.3 \
    # Change some platformio settings
    && platformio settings set enable_telemetry No \
    && platformio settings set check_libraries_interval 1000000 \
    && platformio settings set check_platformio_interval 1000000 \
    && platformio settings set check_platforms_interval 1000000 \
    # Build an empty platformio project to force platformio to install all fw build dependencies
    # The return-code will be non-zero since there's nothing to build.
    && (platformio run -d /opt/pio; echo "Done") \
    && rm -rf /opt/pio/

VOLUME /config
WORKDIR /usr/src/app
