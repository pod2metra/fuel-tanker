# coding: utf-8
import requests
import json
import socket


class Client(object):

    def __init__(self, api_url, username, password, auth_url, tenant_name):
        self.api_url = api_url
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.tenant_name = tenant_name

    @property
    def token(self):
        data = {
            'auth': {
                'tenantName': self.tenant_name,
                'passwordCredentials': {
                    'username': self.username,
                    'password': self.password,
                }
            }
        }
        try:
            resp = requests.post(
                self.auth_url,
                headers={'content-type': 'application/json'},
                data=json.dumps(data)
            ).json()
            if not isinstance(resp, dict):
                raise TypeError
        except (ValueError,
                TypeError,
                socket.timeout,
                requests.exceptions.RequestException):
            return None
        return resp.get('access', {}).get('token', {}).get('id')

    @property
    def request(self):
        session = requests.Session()
        session.headers.update({'X-Auth-Token': self.token})
        return session

    def _post_data(self, url, data):
        resp = self.request.post(url, data=json.dumps(data))
        return resp.text

    def create_release(self, release):
        self._post_data(
            '{api_url}/releases/'.format(api_url=self.api_url), release)
