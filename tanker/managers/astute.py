import os
import yaml


def backup(archive):
    archive.add("/etc/fuel/astute.yaml", "astute/astute.yaml")


def restore(archive):
    dump = archive.extractfile("astute/astute.yaml")
    if not os.path.exists("/etc/fuel/astute.yaml"):
        raise Exception("no astute etc file")
    backup_yaml = yaml.load(dump)
    with open("/etc/fuel/astute.yaml", "r") as current:
        current_yaml = yaml.load(current)
    new_yaml = backup_yaml.copy()
    new_yaml['BOOTSTRAP'] = current_yaml['BOOTSTRAP']
    with open("/etc/fuel/astute.yaml", "w") as new:
        yaml.safe_dump(new_yaml, new, default_flow_style=False)
