from pathlib import Path
import shutil

root_path = Path('.')
hassio_template = root_path / 'template' / 'Dockerfile.hassio'
docker_template = root_path / 'template' / 'Dockerfile'
qemu_path = root_path / 'qemu'
hooks_path = root_path / 'template' / 'hooks'


def copy_hook(arch):
    t = root_path / arch / 'hooks'
    if t.exists():
        shutil.rmtree(t)
    if arch in ('amd64', 'i386'):
        return
    shutil.copytree(hooks_path, t)


def gen_hassio(hassio_arch):
    d = root_path / hassio_arch
    d.mkdir(exist_ok=True)
    temp = hassio_template.read_text()
    target = d / 'Dockerfile.hassio'
    temp = temp.replace('__HASSIO_ARCH__', hassio_arch)
    if qemu_arch is None:
        temp = temp.replace('__COPY_QEMU__', '')
    else:
        qemu = 'qemu-{}-static'.format(qemu_arch)
        line = 'COPY qemu/{0} /usr/bin/{0}'.format(qemu)
        temp = temp.replace('__COPY_QEMU__', line)
    temp = "# This is an auto-generated file, please edit template/Dockerfile.hassio!\n" + temp
    print("Generating {}".format(target))
    target.write_text(temp)
    copy_hook(hassio_arch)


HASSIO_ARCHS = [
    ('amd64', None),
    ('i386', None),
    ('armhf', 'arm'),
    ('aarch64', 'aarch64'),
]
for arch, qemu_arch in HASSIO_ARCHS:
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
        qemu = 'qemu-{}-static'.format(qemu_arch)
        line = 'COPY qemu/{0} /usr/bin/{0}'.format(qemu)
        temp = temp.replace('__COPY_QEMU__', line)
    temp = "# This is an auto-generated file, please edit template/Dockerfile!\n" + temp
    print("Generating {}".format(target))
    target.write_text(temp)
    copy_hook(target_arch)


DOCKER_ARCHS = [
    ('amd64', 'amd64', None),
    ('i386', 'i386', None),
    # ('armhf', 'armhf', 'arm'),  # arm32v6/arm32v7 do not have non-alpine versions of python
    # ('aarch64', 'arm64v8', 'aarch64'),
]

for t, d, q in DOCKER_ARCHS:
    gen_docker(t, d, q)
