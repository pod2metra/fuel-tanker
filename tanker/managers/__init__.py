from . import astute
from . import cobbler
from . import nginx
from . import postgres
from . import puppet
from . import ssh
from . import version


__all__ = [
    "astute",
    "cobbler",
    "nginx",
    "postgres",
    "puppet",
    "ssh",
    "version",
]

MANAGERS = [
    astute,
    cobbler,
    nginx,
    postgres,
    puppet,
    ssh,
    version
]
