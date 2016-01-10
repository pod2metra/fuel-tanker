# coding: utf-8
import os
import contextlib
import tarfile

from cliff import command


class Restore(command.Command):

    def get_parser(self, *args, **kwargs):
        parser = super(Restore, self).get_parser(*args, **kwargs)
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
        if not os.path.isfile(parsed_args.path):
            raise ValueError("Invalid path to backup file")
        with contextlib.closing(tarfile.open(parsed_args.path)) as archive:
            for manager in manager_list:
                manager.restore(archive)
