FROM __DOCKER_ARCH__/ubuntu:focal-20200720

# Environment variables
ENV \
    DEBIAN_FRONTEND="noninteractive" \
    HOME="/root" \
    TERM="xterm-256color" \
    # Fix click python3 lang warning https://click.palletsprojects.com/en/7.x/python3/
    LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"

RUN \
    apt-get update \
    # Use pinned versions so that we get updates with build caching
    && apt-get install -y --no-install-recommends \
        python3=3.8.2-0ubuntu2 \
        python3-pip=20.0.2-5ubuntu1 \
        python3-setuptools=45.2.0-1 \
        python3-pil=7.0.0-4ubuntu0.1 \
        python3-cryptography=2.8-3 \
        iputils-ping=3:20190709-3 \
        git=1:2.25.1-1ubuntu3 \
        curl=7.68.0-1ubuntu2.1 \
    && rm -rf \
        /tmp/* \
        /var/{cache,log}/* \
        /var/lib/apt/lists/*

COPY platformio.ini /opt/pio/

RUN \
    # Ubuntu python3-pip is missing wheel
    pip3 install --no-cache-dir \
        wheel==0.34.2 \
        platformio==4.3.4 \
    # Change some platformio settings
    && platformio settings set enable_telemetry No \
    && platformio settings set check_libraries_interval 1000000 \
    && platformio settings set check_platformio_interval 1000000 \
    && platformio settings set check_platforms_interval 1000000 \
    # Build an empty platformio project to force platformio to install all fw build dependencies
    # The return-code will be non-zero since there's nothing to build.
    # Use upload target so that packages required for uploading also get installed
    && (platformio run -d /opt/pio -t upload; echo "Done") \
    && rm -rf /opt/pio/

VOLUME /config
WORKDIR /usr/src/app
