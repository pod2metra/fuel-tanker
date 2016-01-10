# coding: utf-8
import subprocess
from . import utils


def backup(archive):
    process = subprocess.Popen(
        [
            "dockerctl",
            "shell",
            "cobbler",
            "ls",
            "/var/lib/cobbler/config/systems.d/",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, _ = process.communicate()
    process.wait()
    nodes = stdout.split()
    for node in nodes:
        utils.archivate_container_cmd_output(
            archive,
            "cobbler",
            "cat /var/lib/cobbler/config/systems.d/{0}".format(node),
            "cobbler/systems.d/{0}".format(node))


def restore(archive):
    for member in archive:
        if not member.name.startswith("cobbler/systems.d"):
            continue
        if not member.isfile():
            continue
        name = member.name.rsplit("/", 1)[-1]
        utils.restore_file_in_container(
            archive,
            "cobbler",
            member.name,
            "/var/lib/cobbler/config/systems.d/{0}".format(name),
        )
