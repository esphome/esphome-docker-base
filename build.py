#!/usr/bin/env python3
from dataclasses import dataclass
import subprocess
import argparse
import platform
import shlex
import re
import sys


CHANNEL_DEV = 'dev'
CHANNEL_RELEASE = 'release'
CHANNELS = [CHANNEL_DEV, CHANNEL_RELEASE]

ARCH_AMD64 = 'amd64'
ARCH_ARMV7 = 'armv7'
ARCH_AARCH64 = 'aarch64'
ARCHS = [ARCH_AMD64, ARCH_ARMV7, ARCH_AARCH64]

TYPE_DOCKER = 'docker'
TYPE_HA_ADDON = 'ha-addon'
TYPE_LINT = 'lint'
TYPES = [TYPE_DOCKER, TYPE_HA_ADDON, TYPE_LINT]

BASE_IMAGES = {
    TYPE_DOCKER: "{docker_arch}/debian:buster-20210511-slim",
    TYPE_HA_ADDON: "ghcr.io/hassio-addons/debian-base/{arch}:4.2.1",
    TYPE_LINT: "esphome/esphome-base-{arch}:{tag}",
}


parser = argparse.ArgumentParser()
parser.add_argument("--tag", type=str, required=True, help="The main docker tag to push to. If a version number also adds latest tag")
parser.add_argument("--arch", choices=ARCHS, required=False, help="The architecture to build for")
parser.add_argument("--build-type", choices=TYPES, required=True, help="The type of build to run")
parser.add_argument("--dry-run", action="store_true", help="Don't run any commands, just print them")
subparsers = parser.add_subparsers(help="Action to perform", dest="command", required=True)
build_parser = subparsers.add_parser("build", help="Build the image")
push_parser = subparsers.add_parser("push", help="Tag the already built image and push it to docker hub")
manifest_parser = subparsers.add_parser("manifest", help="Create a manifest from already pushed images")


# only lists some possibilities, doesn't have to be perfect
# https://stackoverflow.com/a/45125525
UNAME_TO_ARCH = {
    "x86_64": ARCH_AMD64,
    "aarch64": ARCH_AARCH64,
    "aarch64_be": ARCH_AARCH64,
    "arm": ARCH_ARMV7,
}


@dataclass(frozen=True)
class DockerParams:
    build_from: str
    build_to: str
    manifest_to: str
    dockerfile: str

    @classmethod
    def for_type_arch_tag(cls, build_type, arch, tag):
        prefix = {
            TYPE_DOCKER: "esphome/esphome-base",
            TYPE_HA_ADDON: "esphome/esphome-hassio-base",
            TYPE_LINT: "esphome/esphome-lint-base"
        }[build_type]

        docker_arch = {
            ARCH_AMD64: "amd64",
            ARCH_ARMV7: "arm32v7",
            ARCH_AARCH64: "arm64v8",
        }[arch]
        build_from = BASE_IMAGES[build_type].format(
            docker_arch=docker_arch,
            arch=arch,
            tag=tag
        )

        build_to = f"{prefix}-{arch}"
        dockerfile = {
            TYPE_DOCKER: "Dockerfile",
            TYPE_HA_ADDON: "Dockerfile.hassio",
            TYPE_LINT: "Dockerfile.lint",
        }[build_type]
        return cls(
            build_from=build_from,
            build_to=build_to,
            manifest_to=prefix,
            dockerfile=dockerfile
        )


def main():
    args = parser.parse_args()

    def run_command(*cmd, ignore_error: bool = False):
        print(f"$ {shlex.join(list(cmd))}")
        if not args.dry_run:
            rc = subprocess.call(list(cmd))
            if rc != 0 and not ignore_error:
                print("Command failed")
                sys.exit(1)

    # detect channel from tag
    match = re.match(r'\d+\.\d+(?:\.\d+)?', args.tag)
    channel = CHANNEL_DEV if match is None else CHANNEL_RELEASE

    tags_to_push = [args.tag]
    if channel == CHANNEL_DEV:
        tags_to_push.append("dev")
    elif channel == CHANNEL_RELEASE:
        tags_to_push.append("latest")

    if args.command == "build":
        # 1. pull cache image
        params = DockerParams.for_type_arch_tag(args.build_type, args.arch, args.tag)
        cache_tag = "latest"
        run_command("docker", "pull", f"{params.build_to}:{cache_tag}", ignore_error=True)

        # 2. register QEMU binfmt (if not host arch)
        is_native = UNAME_TO_ARCH.get(platform.machine()) == args.arch
        if not is_native:
            run_command(
                "docker", "run", "--rm", "--privileged", "multiarch/qemu-user-static:5.2.0-2", 
                "--reset", "-p", "yes"
            )

        # 3. build
        cmd = [
            "docker", "build",
            "--build-arg", f"BUILD_FROM={params.build_from}",
            "--tag", f"{params.build_to}:{args.tag}",
            "--cache-from", f"{params.build_to}:{cache_tag}",
            "--file", params.dockerfile,
        ]
        if args.build_type == TYPE_HA_ADDON:
            cmd += [
                "--build-arg", f"BUILD_ARCH={args.arch}"
            ]
        cmd += ["."]
        run_command(*cmd)
    elif args.command == "push":
        params = DockerParams.for_type_arch_tag(args.build_type, args.arch, args.tag)
        imgs = [f"{params.build_to}:{tag}" for tag in tags_to_push]
        src = imgs[0]
        # 1. tag images
        for img in imgs[1:]:
            run_command(
                "docker", "tag", src, img
            )
        # 2. push images
        for img in imgs:
            run_command(
                "docker", "push", img
            )
    elif args.command == "manifest":
        manifest = DockerParams.for_type_arch_tag(args.build_type, ARCH_AMD64, args.tag).manifest_to

        targets = [f"{manifest}:{tag}" for tag in tags_to_push]
        # 1. Create manifests
        for target in targets:
            cmd = ["docker", "manifest", "create", target] + [
                f"{DockerParams.for_type_arch_tag(args.build_type, arch, args.tag).build_to}:{args.tag}"
                for arch in ARCHS
            ]
            run_command(*cmd)
        # 2. Push manifests
        for target in targets:
            run_command(
                "docker", "manifest", "push", target
            )


if __name__ == "__main__":
    main()
