# coding: utf-8
import os
import contextlib
import tarfile
import datetime

from cliff import command

from tanker import managers


class Backup(command.Command):

    def get_parser(self, *args, **kwargs):
        parser = super(Backup, self).get_parser(*args, **kwargs)
        parser.add_argument(
            "-p",
            "--path_to_backup",
            type=str,
            action="store",
            dest="path",
            required=True,
            help="path to backup dir")
        return parser

    def take_action(self, parsed_args):
        if not os.path.isdir(parsed_args.path):
            raise ValueError("Invalid path to cakup dir")
        now_str = datetime.datetime.now().strftime("%Y_%m_%H_%M_%S")
        backup_name = "backup_{0}.tar.gz".format(now_str)
        backup_path = os.path.join(parsed_args.path, backup_name)
        with contextlib.closing(tarfile.open(backup_path, "w:gz")) as archive:
            for manager in managers.MANAGERS:
                manager.backup(archive)
