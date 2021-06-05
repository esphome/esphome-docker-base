# Maintainer Notes

These docker base images are used by ESPHome and install
all base tools that ESPHome expects as well as platformio
packages for ESP32/ESP8266.

Additionally all packages that can't be easily installed with `pip`
on all platforms but for which a Debian package exists, the base
images are also used.

The base image builds on top of `debian:buster` (changed from Ubuntu
see #16).

The following docker images are built by this repository:

 - `esphome/esphome-base-amd64`
 - `esphome/esphome-base-armv7`
 - `esphome/esphome-base-aarch64`
 - `esphome/esphome-base` (manifest)
 - `esphome/esphome-hassio-base-amd64`
 - `esphome/esphome-hassio-base-armv7`
 - `esphome/esphome-hassio-base-aarch64`
 - `esphome/esphome-hassio-base` (manifest)
 - `esphome/esphome-lint-base`

A new version is released by creating a release on Github. Please
make sure the tag begins with a `v`. For example `v2.3.2`.

Github Actions will automatically build them and publish them to
Docker hub. For example for tag `v2.3.2` the images `esphome/esphome-base-amd64:latest` and `esphome/esphome-base-amd64:2.3.2` will be pushed.

Next the base image value has to be updated in a couple of places:

 - `esphome/.github/workflows/ci-docker.yml`: `base_version=[...]`
 - `esphome/.github/workflows/release-dev.yml`: `base_version=[...]`
 - `esphome/.github/workflows/release.yml`: `base_version=[...]`
 - `esphome/docker/Dockerfile`: `ARG BUILD_FROM=...`
 - `esphome/docker/Dockerfile.dev`: `ARG BUILD_FROM=...`
 - `esphome/docker/Dockerfile.lint`: `ARG BUILD_FROM=...`
 - `hassio/template/addon_config.yaml`: `base_image: [...]`

The helper script `esphome/script/bump-docker-base-version.py` bumps
all versions in the esphome repository. The base image value in the
hassio repository is used by the Development version add-on. Run the
`hassio/script/generate.py` with the argument `dev` after bumping.

## Caching & Dependency Pinning

These baes images use layer caching so that the user doesn't have to
download a full base image every time. However, this means that
docker only updates packages if the relevant Dockerfile `RUN` command
changes.

This means that all packages have to be version pinned.

To view the latest version of a package in one command use

```bash
apt update
PKG=...
apt-cache show $PKG | grep 'Version: ' | sed -E 's/Version: (.*)/\1/' | head -1

for PKG in python3 python3-pip python3-setuptools python3-pil python3-cryptography iputils-ping git curl nginx clang-format-7 clang-tidy-7 patch software-properties-common; do
  vers=$(apt-cache show $PKG | grep 'Version: ' | sed -E 's/Version: (.*)/\1/' | head -1)
  echo "        $PKG=$vers \\"
done
```
