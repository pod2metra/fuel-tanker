# coding: utf-8
import subprocess
from . import utils


def backup(archive):
    utils.archivate_container_cmd_output(
        archive,
        "postgres",
        "sudo -u postgres pg_dumpall",
        "postgres/dump.sql")


def restore(archive):
    dump = archive.extractfile('postgres/dump.sql')
    containers = ["keystone", "nailgun", "ostf"]
    for container in containers:
        subprocess.call([
            "systemctl", "stop", "docker-{0}.service".format(container)
        ])
        utils.exec_cmd_in_container(
            "postgres",
            "sudo -u postgres dropdb --if-exists {0}".format(container))
    process = subprocess.Popen(
        [
            "dockerctl",
            "shell",
            "postgres",
            "sudo",
            "-u",
            "postgres",
            "psql"
        ],
        stdin=subprocess.PIPE,
    )
    process.communicate(str(dump.read()))
    process.wait()
    for container in containers:
        subprocess.call([
            "systemctl", "start", "docker-{0}.service".format(container)
        ])
    utils.exec_cmd_in_container("nailgun", "nailgun_syncdb")
    utils.exec_cmd_in_container("keystone", "keystone-manage db_sync")
