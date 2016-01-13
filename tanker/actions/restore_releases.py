# coding:utf-8
import yaml
from tanker.managers import utils


def add_releases(client, **context):
    data = utils.exec_cmd_in_container(
        "nailgun",
        "cat /usr/share/fuel-openstack-metadata/openstack.yaml")
    fixtures = yaml.load(data)
    base_release_fields = fixtures[0]['fields']
    for fixture in fixtures[1:]:
        data = base_release_fields.copy()
        data.update(fixture['fields'])
        client.create_release(data)
