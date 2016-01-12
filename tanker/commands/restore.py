# coding: utf-8
import os
import contextlib
import tarfile

from cliff import command

from tanker import actions
from tanker import managers
from tanker.clients import nailgun


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

        parser.add_argument(
            "-W",
            "--password",
            type=str,
            action="store",
            dest="password",
            required=True,
            help="Nailgun password")

        return parser

    def take_action(self, parsed_args):
        if not os.path.isfile(parsed_args.path):
            raise ValueError("Invalid path to backup file")
        with contextlib.closing(tarfile.open(parsed_args.path)) as archive:
            for manager in managers.MANAGERS:
                manager.restore(archive)
        nailgun_api = 'http://localhost:8000/api/v1'
        keystone_api = "http://localhost:5000/v2.0/tokens"
        username = "admin"
        tenant_name = "admin"
        post_restore_actions = {
            "client": nailgun.Client(
                nailgun_api,
                username,
                parsed_args.password,
                keystone_api,
                tenant_name,
            )
        }
        for action in actions.ACTIONS:
            action(**post_restore_actions)
