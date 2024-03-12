"""
concept inspired from tweepy binder.py
"""
import re

import requests

import logging
from pyhpcc.__errors import Error
#from pyhpcc.utils import convert_to_utf8_str

re_path_template = re.compile('{\w+}')

log = logging.getLogger('pyHPCC.binder')

import six
def convert_to_utf8_str(arg):
    # written by Michael Norton (http://docondev.blogspot.com/)
    if isinstance(arg, six.text_type):
        arg = arg.encode('utf-8')
    elif not isinstance(arg, bytes):
        arg = six.text_type(arg).encode('utf-8')
    return arg


def wrapper(**config):
    class APIMethod(object):
        api = config['api']
        path = config['path']
        response_type = api.response_type
        payload_list = config.get('payload_list', False)
        allowed_param = config.get('allowed_param', [])
        method = config.get('method', 'POST')
        require_auth = config.get('require_auth', False)
        use_cache = config.get('use_cache', True)
#        session = requests.Session()
#        session.config['Keep-Alive'] = False
        def __init__(self, args, kwargs):
            api = self.api
            self.session = api.auth.session
            # If authentication is required and no credentials
            # are provided, throw an error.
            if self.require_auth and not api.auth:
                raise Error("authentication required")
            self.data = kwargs.pop('data', None)
            self.files = kwargs.pop('files', None)
            self.session.headers = kwargs.pop('headers', {})
            self.build_parameters(args, kwargs)
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
                if arg is None:
                    continue
                if k in self.session.params:
                    raise Error('Multiple values for parameter %s supplied!' % k)

                self.session.params[k] = convert_to_utf8_str(arg)

            log.info("PARAMS: %r", self.session.params)

        def execute(self):
            self.api.cached_result = False

            # Build the request URL
            full_url = self.api.auth.get_url() + self.api.auth.pathDelimiter + self.path + self.response_type
                # Request compression if configured
#            if self.api.compression:
            self.session.headers['Accept-encoding'] = 'gzip'            
#            self.session.headers['Connection']      = 'close'
            # Apply authentication
            if self.api.auth:
                auth = self.api.auth.oauth

            # Execute request
            try:
                resp = self.session.request(self.method,
                                            full_url,
                                            data=self.data,
                                            files=self.files,
                                            timeout=self.api.timeout,
                                            auth=auth)
            except requests.exceptions.Timeout:
                raise requests.exceptions.Timeout
                # Maybe set up for a retry, or continue in a retry loop
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
