#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012 pade (Paul Dassier), TestLink-API-Python-client developers
#
#  Licensed under ???
#  see https://github.com/orenault/TestLink-API-Python-client/issues/4

class TestLinkError(Exception):
    """ Basic error handler
    Return message pass as argument
    """
    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return self.__msg
        