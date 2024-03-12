# -*- coding: utf-8 -*-

"""Handle HPCC client authentication and platform attributes here 


"""
import requests
from requests.auth import HTTPDigestAuth
from pyhpcc.__errors import Error


class auth(object):
    def __init__(self, ip, port, username,
                 password, require_auth=False, protocol='http'):
        self.protDelimiter = "://"
        self.portDelimiter = ':'
        self.pathDelimiter = '/'
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.protocol = protocol
        self.oauth = (self.username, self.password)
        self.session = requests.Session()

    def get_url(self):
        return self.protocol + self.protDelimiter + self.ip + self.portDelimiter + str(self.port)

    def get_username(self):
        return self.username

    def get_verified(self):
        try:
            url = self.get_url()

            r = requests.get(url=url, auth=self.oauth)
            if r.status_code != 200:
                raise ('Invalid Credentials')

        except Exception:
            e = "error response: status code = %s , error message %s" % (r.status_code, r.content)
            raise Error(e)
