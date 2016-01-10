# coding: utf-8
from . import utils


def backup(archive):
    utils.archive_dirs(archive, "/etc/fuel", "version")


def restore(archive):
    utils.extract_tag_to(archive, "version", "/etc/fuel/")
