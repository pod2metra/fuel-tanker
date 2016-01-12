# coding:utf-8
import yaml
from tanker.managers import utils


def add_releases(client, **context):
    data = utils.exec_cmd_in_container(
        "nailgun",
        "cat /usr/share/fuel-openstack-metadata/openstack.yaml")
    fixtures = yaml.load(data)
    for fixture in fixtures:
        data = fixture['fields']
        data['state'] = data.get('state') or "available"
        client.create_release(data)
