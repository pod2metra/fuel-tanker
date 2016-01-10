# coding: utf-8
from . import utils


def backup(archive):
    archive.add("/root/.ssh/", "ssh/")


def restore(archive):
    utils.extract_tag_to(archive, "ssh", "/root/.ssh/")
