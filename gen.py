from pathlib import Path
import shutil

root_path = Path('.')
hassio_template = root_path / 'template' / 'Dockerfile.hassio'
docker_template = root_path / 'template' / 'Dockerfile'
qemu_path = root_path / 'qemu'

patch_aarch64 = r""" \
    \
    && rm -rf /root/.platformio/packages/toolchain-xtensa32 \
    && curl -sSL -o /toolchain-xtensa32.tar.gz \
         https://github.com/esphome/esphome-docker-base/releases/download/v1.4.0/toolchain-xtensa32.tar.gz \
    && tar -xzvf /toolchain-xtensa32.tar.gz -C /root/.platformio/packages/ \
    && rm /toolchain-xtensa32.tar.gz \
    \
    && rm -rf /root/.platformio/packages/toolchain-xtensa \
    && curl -sSL -o /toolchain-xtensa.tar.gz \
         https://github.com/esphome/esphome-docker-base/releases/download/v1.4.0/toolchain-xtensa.tar.gz \
    && tar -xzvf /toolchain-xtensa.tar.gz -C /root/.platformio/packages/ \
    && rm /toolchain-xtensa.tar.gz
"""


def replace_patch_aarch64(temp, arch):
    if arch == 'aarch64':
        return temp.replace('__PATCH_AARCH64__', patch_aarch64)
    else:
        return temp.replace('__PATCH_AARCH64__', '')


def gen_hassio(hassio_arch, base_arch):
    d = root_path / hassio_arch
    d.mkdir(exist_ok=True)
    temp = hassio_template.read_text()
    target = d / 'Dockerfile.hassio'
    temp = temp.replace('__HASSIO_ARCH__', hassio_arch)
    temp = temp.replace('__UBUNTU_BASE_ARCH__', base_arch)
    temp = replace_patch_aarch64(temp, hassio_arch)
    temp = "# This is an auto-generated file, please edit template/Dockerfile.hassio!\n" + temp
    print("Generating {}".format(target))
    target.write_text(temp)


HASSIO_ARCHS = [
    ('amd64', 'amd64'),
    ('i386', 'i386'),
    ('armv7', 'armv7'),
    ('aarch64', 'aarch64'),
]
for arch, base_arch in HASSIO_ARCHS:
    gen_hassio(arch, base_arch)


def gen_docker(target_arch, docker_arch, qemu_arch):
    d = root_path / target_arch
    d.mkdir(exist_ok=True)
    temp = docker_template.read_text()
    target = d / 'Dockerfile'
    temp = temp.replace('__DOCKER_ARCH__', docker_arch)
    temp = replace_patch_aarch64(temp, target_arch)
    if qemu_arch is None:
        temp = temp.replace('__COPY_QEMU__', '')
    else:
        qemu = 'qemu-{}-static'.format(qemu_arch)
        line = 'COPY qemu/{0} /usr/bin/{0}'.format(qemu)
        temp = temp.replace('__COPY_QEMU__', line)
    temp = "# This is an auto-generated file, please edit template/Dockerfile!\n" + temp
    print("Generating {}".format(target))
    target.write_text(temp)


DOCKER_ARCHS = [
    ('amd64', 'amd64', None),
    ('i386', 'i386', None),
    ('armv7', 'arm32v7', 'arm'),
    ('aarch64', 'arm64v8', 'aarch64'),
]

for t, d, q in DOCKER_ARCHS:
    gen_docker(t, d, q)
