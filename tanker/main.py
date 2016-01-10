import sys

from cliff import app
from cliff import commandmanager


def main(argv=sys.argv[1:]):
    myapp = app.App(
        description='',
        version='',
        command_manager=commandmanager.CommandManager('manager'),
        deferred_help=True,
    )
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
