# coding: utf-8
from . import utils


_PARAMS = [
    ("/var/lib/fuel/keys/master/nginx/nginx.crt", "nginx.crt"),
    ("/var/lib/fuel/keys/master/nginx/nginx.key", "nginx.key"),
]


def backup(archive):
    for path, tag in _PARAMS:
        utils.archivate_container_cmd_output(
            archive, "nginx", "cat {0}".format(path), "nginx/{0}".format(tag))


def restore(archive):
    for path, tag in _PARAMS:
        utils.restore_file_in_container(archive, "nginx", tag, path)
