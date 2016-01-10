# coding: utf-8
from . import utils


def backup(archive):
    utils.archive_dirs(archive, "/etc/puppet", "puppet")


def restore(archive):
    utils.extract_tag_to(archive, "puppet", "/etc/puppet")
