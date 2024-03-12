# -*- coding: utf-8 -*-

# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

import re

from six.moves.urllib.parse import quote
import requests

import logging
from pyhpcc.__errors import Error
from pyhpcc.utils import convert_to_utf8_str

re_path_template = re.compile('{\w+}')

log = logging.getLogger('pyHPCC.binder')


def wrapper(**config):
    class APIMethod(object):

        api = config['api']
        response_type = api.response_type
        method = config.get('method', 'POST')
        require_auth = config.get('require_auth', False)
        use_cache = config.get('use_cache', True)
        session = requests.Session()

        def __init__(self, args, kwargs):
            api = self.api
            # If authentication is required and no credentials
            # are provided, throw an error.
            if self.require_auth and not api.auth:
                raise Error("authentication required")
            self.post_data = kwargs.pop('post_data', None)
            self.session.headers = kwargs.pop('headers', {})
            self.build_parameters(args, kwargs)

        #            self.session.headers['Host'] = self.

        def build_parameters(self, args, kwargs):
            self.session.params = {}
            for idx, arg in enumerate(args):
                if arg is None:
                    continue
                try:
                    self.session.params[self.allowed_param[idx]] = convert_to_utf8_str(arg)
                except IndexError:
                    raise Error('Too many parameters supplied!')
            for k, arg in list(kwargs.items()):
                # for k, arg in kwargs.items():
                if arg is None:
                    continue
                if k in self.session.params:
                    raise Error('Multiple values for parameter %s supplied!' % k)

                self.session.params[k] = convert_to_utf8_str(arg)

            log.info("PARAMS: %r", self.session.params)

        def execute(self):
            self.api.cached_result = False

            # Build the request URL
            url = self.api.auth.get_url() + self.api.auth.pathDelimiter + self.api.definition + self.api.auth.pathDelimiter + self.api.roxie_port + self.api.auth.pathDelimiter + self.api.searchservice + self.api.auth.pathDelimiter + self.response_type
            full_url = url

            # Apply authentication
            if self.api.auth:
                auth = self.api.auth.oauth

            # Execute request
            try:
                resp = self.session.request(self.method,
                                            full_url,
                                            data=self.post_data,
                                            timeout=self.api.timeout,
                                            auth=auth)
            except Exception as e:
                raise Error('Failed to send request: %s' % e)

            # If an error was returned, throw an exception
            self.api.last_response = resp
            if resp.status_code and not 200 <= resp.status_code < 300:
                try:
                    error_msg, api_error_code = \
                        self.parser.parse_error(resp.text)
                except Exception:
                    error_msg = "error response: status code = %s , error message %s" % (resp.status_code, resp.content)
                    raise Error(error_msg)

            # Parse the response payload
            result = resp

            return result

    def _call(*args, **kwargs):
        method = APIMethod(args, kwargs)
        return method.execute()

    return _call


class roxie(object):
    """HPCC API"""

    def __init__(self, auth, searchservice, roxie_port, timeout=1200, response_type='json',definition = 'submit'):
        """ Api instance Constructor
        :param timeout: delay before to consider the request as timed out in seconds, default:60
        :raise TypeError: If the given parser is not a ModelParser instance.
        """
        self.auth = auth
        self.timeout = timeout
        self.response_type = response_type
        self.definition = 'WsEcl/'+definition +'/query'
        self.searchservice = searchservice
        self.roxie_port = roxie_port

    @property
    def roxie_call(self):
        """ :reference: http://ip:port/WsEcl/submit/query/roxie/roxie_service/json
        
        """
        return wrapper(
            api=self)
