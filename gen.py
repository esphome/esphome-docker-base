from pathlib import Path
import shutil

root_path = Path('.')
hassio_template = root_path / 'template' / 'Dockerfile.hassio'
docker_template = root_path / 'template' / 'Dockerfile'
qemu_path = root_path / 'qemu'
build_dir = root_path / 'build'


def gen_hassio(hassio_arch):
    d = build_dir / hassio_arch
    d.mkdir(exist_ok=True, parents=True)
    temp = hassio_template.read_text()
    target = d / 'Dockerfile.hassio'
    temp = temp.replace('__HASSIO_ARCH__', hassio_arch)
    temp = "# This is an auto-generated file, please edit template/Dockerfile.hassio!\n" + temp
    print("Generating {}".format(target))
    target.write_text(temp)


HASSIO_ARCHS = [
    'amd64',
    'armv7',
    'aarch64',
]
for arch in HASSIO_ARCHS:
    gen_hassio(arch)


def gen_docker(target_arch, docker_arch):
    d = build_dir / target_arch
    d.mkdir(exist_ok=True, parents=True)
    temp = docker_template.read_text()
    target = d / 'Dockerfile'
    temp = temp.replace('__DOCKER_ARCH__', docker_arch)
    temp = "# This is an auto-generated file, please edit template/Dockerfile!\n" + temp
    print("Generating {}".format(target))
    target.write_text(temp)


DOCKER_ARCHS = [
    ('amd64', 'amd64'),
    ('armv7', 'arm32v7'),
    ('aarch64', 'arm64v8'),
]

for t, d in DOCKER_ARCHS:
    gen_docker(t, d)
