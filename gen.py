from pathlib import Path
import shutil

root_path = Path('.')
hassio_template = root_path / 'template' / 'Dockerfile.hassio'
docker_template = root_path / 'template' / 'Dockerfile'
qemu_path = root_path / 'qemu'

def copy_hook(arch):
    t = root_path / arch / 'hooks'
    shutil.rmtree(t)
    shutil.copytree(root_path / 'hooks', t)

def gen_hassio(hassio_arch):
    d = root_path / hassio_arch
    d.mkdir(exist_ok=True)
    temp = hassio_template.read_text()
    target = d / 'Dockerfile.hassio'
    temp = temp.replace('__HASSIO_ARCH__', hassio_arch)
    print("Generating {}".format(target))
    target.write_text(temp)
    copy_hook(hassio_arch)

HASSIO_ARCHS = ['amd64', 'i386', 'armhf', 'aarch64']
for arch in HASSIO_ARCHS:
    gen_hassio(arch)

def gen_docker(target_arch, docker_arch, qemu_arch):
    d = root_path / target_arch
    d.mkdir(exist_ok=True)
    temp = docker_template.read_text()
    target = d / 'Dockerfile'
    temp = temp.replace('__DOCKER_ARCH__', docker_arch)
    if qemu_arch is None:
        temp = temp.replace('__COPY_QEMU__', '')
    else:
        line = 'COPY qemu/qemu-{}-static /usr/bin/'.format(qemu_arch)
        temp = temp.replace('__COPY_QEMU__', line)
    print("Generating {}".format(target))
    target.write_text(temp)
    copy_hook(target_arch)
    if qemu_arch is not None:
        f = 'qemu-{}-static'.format(qemu_arch)
        shutil.copy(qemu_path / f, d / f)

DOCKER_ARCHS = [
    ('amd64', 'amd64', None),
    ('i386', 'i386', None),
    ('armhf', 'arm32v7', 'arm'),
    ('aarch64', 'arm64v8', 'aarch64')
]

for t, d, q in DOCKER_ARCHS:
    gen_docker(t, d, q)
