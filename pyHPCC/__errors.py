# -*- coding: utf-8 -*-

class Error(Exception):
    
    def __init__(self, message):

        self.message = message
        Exception.__init__(self, message)
    def get_msg(self):
        return self._message

    
