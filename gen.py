from pathlib import Path
import shutil

root_path = Path('.')
hassio_template = root_path / 'template' / 'Dockerfile.hassio'
docker_template = root_path / 'template' / 'Dockerfile'
qemu_path = root_path / 'qemu'
build_dir = root_path / 'build'


def gen_hassio(hassio_arch, base_arch, qemu_arch):
    d = build_dir / hassio_arch
    d.mkdir(exist_ok=True, parents=True)
    temp = hassio_template.read_text()
    target = d / 'Dockerfile.hassio'
    temp = temp.replace('__HASSIO_ARCH__', hassio_arch)
    temp = temp.replace('__DEBIAN_BASE_ARCH__', base_arch)
    if qemu_arch is None:
        temp = temp.replace('__COPY_QEMU__', '')
    else:
        qemu = 'qemu-{}-static'.format(qemu_arch)
        line = 'COPY qemu/{0} /usr/bin/{0}'.format(qemu)
        temp = temp.replace('__COPY_QEMU__', line)
    temp = "# This is an auto-generated file, please edit template/Dockerfile.hassio!\n" + temp
    print("Generating {}".format(target))
    target.write_text(temp)


HASSIO_ARCHS = [
    ('amd64', 'amd64', None),
    ('i386', 'i386', None),
    ('armv7', 'armv7', 'arm'),
    ('aarch64', 'aarch64', 'aarch64'),
]
for arch, base_arch, qemu_arch in HASSIO_ARCHS:
    gen_hassio(arch, base_arch, qemu_arch)


def gen_docker(target_arch, docker_arch, qemu_arch):
    d = build_dir / target_arch
    d.mkdir(exist_ok=True, parents=True)
    temp = docker_template.read_text()
    target = d / 'Dockerfile'
    temp = temp.replace('__DOCKER_ARCH__', docker_arch)
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
