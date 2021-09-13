# Use --build-arg BUILD_FROM to set this
# Defined in build.py:BASE_IMAGES

ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN \
    apt-get update \
    # Use pinned versions so that we get updates with build caching
    && apt-get install -y --no-install-recommends \
        python3=3.9.2-3 \
        python3-pip=20.3.4-4 \
        python3-setuptools=52.0.0-4 \
        python3-pil=8.1.2+dfsg-0.3 \
        python3-cryptography=3.3.2-1 \
        iputils-ping=3:20210202-1 \
        git=1:2.30.2-1 \
        curl=7.74.0-1.3+b1 \
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
        wheel==0.36.2 \
        platformio==5.2.0 \
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
