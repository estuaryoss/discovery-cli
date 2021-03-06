import re

import requests
from requests.auth import HTTPBasicAuth


class RestApiService:
    def __init__(self, connection):
        self.conn = connection

    def about(self):
        endpoint = "/about"
        url_format = f"{self.conn.get('homePageUrl')}{endpoint}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'),
                                auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))

        if response.status_code != 200:
            raise BaseException("Error: Http code: {}. Http body: {}".format(response.status_code, response.text))

        return response.json()

    def ping(self):
        endpoint = "/ping"
        url_format = f"{self.conn.get('homePageUrl')}{endpoint}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'),
                                auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))

        if response.status_code != 200:
            raise BaseException("Error: Http code: {}. Http body: {}".format(response.status_code, response.text))

        return response.json()

    def get_commands(self):
        endpoint = "/agents/commands"
        url_format = f"{self.conn.get('homePageUrl')}{endpoint}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'),
                                auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))

        # error, server sent non 20x code
        if not re.search('^20\d$', str(response.status_code)):
            print(response.json())
            return {'description': []}

        body = response.json()

        # error, the type should be dict
        if isinstance(body['description'], str):
            print(body.get('description'))
            return {'description': []}

        return body

    def get_eureka_apps(self):
        endpoint = "/eureka/apps"
        url_format = f"{self.conn.get('homePageUrl')}{endpoint}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'),
                                auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))

        # error, server sent non 20x code
        if not re.search('^20\d$', str(response.status_code)):
            print(response.json())
            return {'description': {}}

        body = response.json()

        # error, the type should be dict
        if isinstance(body['description'], str):
            print(body.get('description'))
            return {'description': {}}

        return body

    def get_connection(self):
        return self.conn
