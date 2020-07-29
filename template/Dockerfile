FROM __DOCKER_ARCH__/ubuntu:bionic-20200713

__COPY_QEMU__

RUN \
    apt-get update \
    # Use pinned versions so that we get updates with build caching
    && apt-get install -y --no-install-recommends \
        python3=3.6.7-1~18.04 \
        python3-pip=9.0.1-2.3~ubuntu1.18.04.1 \
        python3-setuptools=39.0.1-2 \
        python3-pil=5.1.0-1ubuntu0.3 \
        python3-cryptography=2.1.4-1ubuntu1.3 \
        iputils-ping=3:20161105-1ubuntu3 \
        git=1:2.17.1-1ubuntu0.7 \
        curl=7.58.0-2ubuntu3.9 \
    && rm -rf \
        /tmp/* \
        /var/{cache,log}/* \
        /var/lib/apt/lists/*

# Fix click python3 lang warning https://click.palletsprojects.com/en/7.x/python3/
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

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
