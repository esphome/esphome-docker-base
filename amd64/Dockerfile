FROM amd64/python:2.7-slim



RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/*

COPY platformio.ini /opt/pio/

RUN \
    pip install --no-cache-dir --no-binary :all: platformio \
    \
    && platformio settings set enable_telemetry No \
    && platformio settings set check_libraries_interval 1000000 \
    && platformio settings set check_platformio_interval 1000000 \
    && platformio settings set check_platforms_interval 1000000 \
    \
    && (platformio run -d /opt/pio; echo "Done") \
    && rm -rf /opt/pio/

VOLUME /config
WORKDIR /usr/src/app
